# TorchSystem.

This framework will help you to create powerful and scalable systems using the PyTorch library. It is designed under the principles of domain driven design (DDD) and includes built-in message patterns and a robust dependency injection system. It enables the creation of stateless, modular service layers and robust domain models. This design facilitates better separation of concerns, testability, and scalability, making it ideal for complex IA training systems. You can find the full documentation here: [mr-mapache.github.io/torch-system/](https://mr-mapache.github.io/torch-system/)


## Table of contents:

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#instalation)
- [Example](#example)
- [License](#license)

## Introduction

In domain driven design, an aggregate is a cluster of associated objects that we treat as a unit for the purpose of data changes. It acts as a boundary around its constituent objects, encapsulating their behavior and ensuring that all changes to its state occur through well-defined entry points.

In the context of deep learning, a model not only consists of a neural network but also a set of associated objects that are necessary for the tasks it performs, such as loss functions, tokenizers, classification heads etc. This cluster of objects defines an aggregate.

While aggregates are in charge of data, in order to perform actions, we need to define services. Services are stateless operations that fulfill domain-specific tasks. For example, when training a neural network, the model doesn't own the data on which it is trained or how the training is performed. The training process is a stateless operation that resides outside the model and should be defined as a service.

Services may produce data, such as events, metrics, or logs, that are not their responsibility to handle. This introduces the need for a messaging system that allows services to communicate with each other.

With all this in mind, the need for a well-defined framework that defines aggregates and handles service interactions becomes evident. While it is up to the developer to define his domain, this framework provides a set of tools to facilitate their implementation.

## Installation

To install the framework, you can use pip:

```bash
pip install torchsystem
```

## Features

- **Aggregates**: Define the structure of your domain by grouping related entities and enforcing consistency within their boundaries. They encapsulate both data and behavior, ensuring that all modifications occur through controlled operations.

- **Domain Events**: Aggregates can produce and consume domain events, which signal meaningful changes in the system or trigger actions elsewhere. Exceptions are supported to be treated as domain events, allowing them to be enqueued and handled or raised as needed. This makes it trivial to implement features like early stopping (Just enqueue an exception and raise it when needed).

- **Registry**: The registry module allows you to treat your models as entities by providing a way to calculate locally unique hashes for them that can act as their identifier. This module also provides several other utilities to help you handle the data from your domain.

- **Dependency Injection**: The framework provides a robust dependency injection system that allows you to define and inject dependencies. This enables you to define your logic in terms of interfaces and inject implementations later. 

- **Compilers**: Building aggregates can be a complex process. In the context of deep learning, aggregates not only need to be built but also compiled, making compilation an integral part of the construction process. This framework provides a Compiler class to help define and manage the compilation process for your aggregates

- **Services**: Define stateless operations that fulfill domain-specific tasks using ubiquitous language. 

- **Producers/Consumers**: Events produced by services can be delivered by producers to several consumers. This allows you to decouple services and define complex interactions between them. 

- **Publisher/Subscriber**: Data also can be delivered with the publisher/subscriber pattern. Publishers can send data to subscribers using a topic-based system.


## Example

Let's build a simple training system using the framework. First, we can define our domain with protocols, while this is not strictly necessary it's a good practice to define the interfaces first.

```python 
# src/domain.py
from typing import Any
from typing import Protocol 

from torch import Tensor
from torch.nn import Module
from torchsystem import Events

class Model(Protocol):
    id: Any
    phase: str
    epoch: int
    events: Events 
    nn: Module
    criterion: Module
    optimizer: Module
    
    def fit(self, *args, **kwargs) -> Any:...

    def evaluate(self, *args, **kwargs) -> Any:...

class Metric(Protocol):
    name: str
    value: Any

class Metrics(Protocol):

    def update(self, *args, **kwargs) -> None:...

    def compute(self) -> Sequence[Metric]:...

class Loader(Protocol):

    def __iter__(self) -> Iterator[tuple[Tensor, Tensor]]:...
```

Notice that we didn't define any implementation. Of course, you can just implement it right away, but let's define a training service first. Service handlers and events produced in the services should be modeled using ubiquitous language. Under this idea, the framework provides a way to invoke services or produce events using their names. This is completely optional, like everything in the library, and you can invoke services handlers and dispatch events directly.

The training service can be implemented as follows:

```python
# src/services/training.py
from typing import Sequence 

from torch import inference_mode
from torchsystem import Depends
from torchsystem.services import Service
from torchsystem.services import Producer, event

from src.domain import Model
from src.domain import Loader
from src.domain import Metric, Metrics 

service = Service() 
producer = Producer() 

@service.handler
def iterate(model: Model, loaders: Sequence[tuple[str, Loader]], metrics: Metrics):
    for phase, loader in loaders:
        train(model, loader, metrics) if phase == 'train' else validate(model, loader, metrics)
    train(model, loader, metrics) if phase == 'train' else validate(model, loader, metrics)
    producer.dispatch(Iterated(model, loaders))

@event
class Iterated:
    model: Model
    loaders: Sequence[tuple[str, Loader]] # We put this on events because you may want to store info about the
                                          # data you used during training.

def device() -> str:
    raise NotImplementedError("Override this dependency with a concrete implementation")

@service.handler
def train(model: Model, loader: Loader, metrics: Metrics, device: str = Depends(device)):
    model.phase = 'train'
    for batch, (input, target) in enumerate(loader, start=1):
        input, target = input.to(device), target.to(device)
        prediction, loss = model.fit(input, target)
        metrics.update(batch, loss, prediction, target)
    sequence = metrics.compute()
    producer.dispatch(Trained(model, loader, metrics))

@service.handler
def validate(model: Model, loader: Loader, metrics: Metrics, device: str = Depends(device)):
    model.phase = 'evaluation'
    with inference_mode():
        for batch, (input, target) in enumerate(loader, start=1):
            input, target = input.to(device), target.to(device)
            prediction, loss = model.evaluate(input, target)
            metrics.update(batch, loss, prediction, target)
        sequence = metrics.compute()
    producer.dispatch(Trained(model, loader, metrics))

@event
class Trained:
    model: Model
    loader: Loader
    metrics: Sequence[Metric]

@event
class Validated:
    model: Model
    loader: Loader
    metrics: Sequence[Metric]
```

And that's it! A simple training system. Notice that it is completely decoupled from the implementation of the domain. It's only task is to orchestrate the training process and produce events from it. It doesn't provide any storage logic or data manipulation, only stateless training logic. Now you can now build a whole data storage system, logging or any other service you need around this simple service.

Let's create a simple tensorboard consumer for this service:

```python
# src/services/tensorboard.py
from torchsystem import Depends
from torchsystem.services import Consumer
from torch.utils.tensorboard.writer import SummaryWriter
from src.services.training import (
    Trained,
    Validated
)

consumer = Consumer()

def writer() -> SummaryWriter:
    raise NotImplementedError("We don't want to handle the writer here!!!, will be injected later in the application layer") 


@consumer.handler
def deliver_metrics(event: Trained | Validated, writer: SummaryWriter = Depends(writer)):
    for metric in event.metrics:
        writer.add_scalar(f'{event.model.id}/{metric.name}/{event.model.phase}', metric.value, event.model.epoch)

    # When you pass an Union of types as annotation, the consumer will register the handler for all types in the Union
    # automatically. This is a good way to handle events that share the same logic.
```

Since several consumers can consume from the same producer, you can plug any service you want to the training system. The service don't need to know who is consuming the events it produces. This is known a dependency inversion principle. You can now build a whole system around this simple training service. All kind of logic can be implemented from here, from weights storage to early stopping. Let's create an early stopping service:

```python
# src/services/earlystopping.py
from torchsystem.services import Subscriber
from torchsystem.services import Consumer

from src.services.training import Metric
from src.services.training import Trained, Validated

subscriber = Subscriber()
consumer = Consumer()

@consumer.handler
def deliver_metrics(event: Trained | Validated):
    for metric in event.metrics:
        try:
            subscriber.receive(metric, metric.name)
        except StopIteration:
            event.model.events.enqueue(StopIteration) # Exceptions are also supported as domain events
                                                      # If you prefer you can create a domain event for this
                                                      # and enqueue it here.
@subscriber.subscribe('loss')
def on_low_loss(metric: Metric):
    if metric.value < 0.001:
        raise StopIteration # Built-in exception from Python
    
@subscriber.subscribe('accuracy')
def on_high_accuracy(metric: Metric):
    if metric.value > 0.995:
        raise StopIteration # Exceptions are a good way to propagate information backwards in the system.
```

This is a simple early stopping service. It listens to the metrics produced by the training service and raises a StopIteration exception when the loss is low enough or the accuracy is high. The exception is enqueued in the model events and can be raised again when needed, for example in a `onepoch` hook in the aggregate. A `Publisher` could also be used to send the messages to the subscribers, but it wasn't necessary in this case.

Now we are going to implement a simple classifier aggregate in order to train a neural network for image classification tasks.

```python
# src/classifier.py
from torch import argmax
from torch import Tensor 
from torch.nn import Module
from torch.nn import Flatten
from torch.optim import Optimizer
from torchsystem.domain import Event
from torchsystem.domain import Aggregate
from torchsystem.registry import gethash

class Classifier(Aggregate): 
    def __init__(self, nn: Module, criterion: Module, optimizer: Optimizer):
        super().__init__()
        self.epoch = 0
        self.nn = nn
        self.criterion = criterion
        self.optimizer = optimizer 
        self.flatten = Flatten()

    @property
    def id(self) -> str:
        return gethash(self.nn) # This will return an identifier for the aggregate root 

    def forward(self, input: Tensor) -> Tensor:
        input = self.flatten(input)
        return self.nn(input)
    
    def loss(self, output: Tensor, target: Tensor) -> Tensor:
        return self.criterion(output, target)
    
    def fit(self, input: Tensor, target: Tensor) -> tuple[Tensor, Tensor]:
        self.optimizer.zero_grad()
        output = self(input)
        loss = self.loss(output, target)
        loss.backward()
        self.optimizer.step()
        return argmax(output, dim=1), loss # returns classification predictions and their loss

    def evaluate(self, input: Tensor, target: Tensor) -> tuple[Tensor, Tensor]:
        output = self(input)
        return argmax(output, dim=1), self.loss(output, target)
    
    def onepoch(self):
        # Hook that will be called after the epoch attribute is updated. The aggregate handle this
        # automatically for epochs and phase.
        self.events.commit() # This will raise the StopIteration exception when the epoch is over
```

As you see, aggregates is just a simple facade to encapsulate things you already knew. Aggregates have also the capability to handle domain events or domain exceptions. 

```python
class SomeDomainEvent(Event):...
# A simple class can represent a domain event.

class DomainException(Exception):...
# Exceptions are also supported as domain events.
# If no handler is found, they will be raised when the event queue is commited.

class DomainEventWithData(Event):
    # They also can carry data
    def __init__(self, data: Any):
        self.data = data

class DomainEventWithIgnoredData(Event):
    def __init__(self, data: Any):
        self.data = data

class Classifier(Aggregate): 
    def __init__(self, nn: Module, criterion: Module, optimizer: Optimizer):
        super().__init__()        
        self.events.handlers[SomeDomainEvent] = lambda: print('SomeDomainEvent handled!')
        self.events.handlers[DomainException] = lambda: print('DomainException handled!')
        self.events.handlers[DomainEventWithData] = lambda event: print(f'DomainEventWithData handled with data: {event.data}')
        self.events.handlers[DomainEventWithIgnoredData] = lambda: print(f'DomainEventWithIgnoredData handled')
        # Usually you need to define the handlers outside the aggregate and pass them in the building process. But
        # This is an example of how you can handle complex domain logic within the aggregate.
        ...
```

The `Classifier` aggregate we just created can be built and compiled in a simple way. However, you will find yourself in situations where you need to pick a torch backend, create and clean multiprocessing resources, pickle modules, etc., and you will need a tool to build the aggregate and compile it. 

I will implement a compilation pipeline, just to show you how to use the compiler:

```python
# src/services/compilation.py
from logging import getLogger
from torch.nn import Module
from torch.optim import Optimizer
from torchsystem import Depends
from torchsystem.compiler import compile
from torchsystem.compiler import Compiler 
from src.classifier import Classifier

logger = getLogger(__name__)
compiler = Compiler[Classifier]()

def device() -> str:...

def epoch() -> int:
    return 10 # Just for the sake of the example

@compiler.step
def build_classifier(model: Module, criterion: Module, optimizer: Optimizer):
    logger.info(f'Building Classifier') 
    return Classifier(model, criterion, optimizer)

@compiler.step
def move_to_device(classifier: Classifier, device = Depends(device)):
    logger.info(f'Moving classifier to device: {device}')
    return classifier.to(device)

@compiler.step
def compile_classifier(classifier: Classifier):
    logger.info(f'Compiling classifier')
    return compile(classifier)

@compiler.step
def get_current_epoch(classifier: Classifier, epoch: int = Depends(epoch)):
    # Implement this with some database query or api call using the classifier.id
    classifier.epoch = epoch
    return classifier
```

Finally, you can put all together in the application layer as follows:

```python
# src/main.py

from torch import cuda
from torch.utils.tensorboard.writer import SummaryWriter

from src.services import (
    training,
    tensorboard,
    earlystopping
)

model = MLP(...)
criterion = CrossEntropyLoss(...)
optimizer = Adam(...)
metrics = Metrics(...)
loaders = [
    ('train', DataLoader(...)),
    ('validation', DataLoader(...))
]

def device():
    return 'cuda' if cuda.is_available() else 'cpu'

def summary_writer():
    writter = SummaryWriter(...)
    yield writter
    writter.close()

training.service.dependency_overrides[training.device] = device
compilation.compiler.dependency_overrides[compilation.device] = device
tensorboard.consumer.dependency_overrides[tensorboard.writer] = summary_writer

...

classifier = compilation.compiler.compile(model, criterion, optimizer)

training.service.handle('iterate', classifier, loaders, metrics)

...
```

This is a simple example of how to build a training system using the framework. Since services can be called by their name, you can easily write a REST API with CQS (Command Query Segregation) or a CLI interfaces for your training system. The possibilities are endless. 

## License

This project is licensed under the MIT License - Use it as you wish in your projects. 