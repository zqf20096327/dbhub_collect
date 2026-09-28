# Equinox [![Build Status](https://dev.azure.com/jet-opensource/opensource/_apis/build/status/jet.equinox?branchName=master)](https://dev.azure.com/jet-opensource/opensource/_build/latest?definitionId=4?branchName=master) [![release](https://img.shields.io/github/release/jet/equinox.svg)](https://github.com/jet/equinox/releases) [![NuGet](https://img.shields.io/nuget/vpre/equinox)](https://www.nuget.org/packages/Equinox/) [![license](https://img.shields.io/github/license/jet/Equinox.svg)](LICENSE) ![code size](https://img.shields.io/github/languages/code-size/jet/equinox.svg) [![docs status](https://img.shields.io/badge/DOCUMENTATION-WIP-important.svg?style=popout)](DOCUMENTATION.md) [![Discord](https://img.shields.io/discord/514783899440775168?color=blue&label=Chat%20in%20equinox%20on%20DDD-CQRS-ES%20Discord)](https://discord.gg/sEZGSHNNbH)

Equinox is a set of low dependency libraries that allow for event-sourced processing against stream-based stores handling:
* Snapshots
* Caching
* [Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)

**Not a framework**; *you* compose the libraries into an architecture that fits your apps' evolving needs. 

It does not and will not handle projections and subscriptions. See [Propulsion](https://github.com/jet/propulsion) for that.

# Table of Contents

* [Getting Started](#getting-started)
* [Design Motivation](#design-motivation)
* [Features](#features)
* [Currently Supported Data Stores](#currently-supported-data-stores)
* [Components](#components)
  * [Core library](#core-library)
  * [Serialization Support](#serialization-support)
  * [Data Store Libraries](#data-store-libraries)
  * [Projection Libraries](#projection-libraries)
  * [Tools](#tools)
  * [Starter Project Templates and Sample Applications](#starter-project-templates-and-sample-applications)
* [Overview](#overview)
* [Templates](#templates)
* [Samples](#samples)
* [Building](#building)
* [Releasing](#releasing)
* [FAQ](#faq)
* [Acknowledgements](#acknowledgements)
* [Further Reading](#further-reading)

# Getting Started

- If you want to start with code samples that run in F# interactive, [there's a simple `Counter` example using `Equinox.MemoryStore`](https://github.com/jet/equinox/blob/master/samples/Tutorial/Counter.fsx#L20)
- If you are experienced with event sourcing, CosmosDB and F#, you might gain most from this [100 LOC end-to-end example using CosmosDB](https://github.com/jet/equinox/blob/master/samples/Tutorial/Cosmos.fsx#L42) 
- If you are familiar with basic event sourcing mechanisms and want a meatier example of applying Equinox to a problem, [Einar Norðfjörð](https://github.com/nordfjord)'s article, [The Equinox Programming model](https://nordfjord.io/2022/12/05/equinox.html) walks through a [complete end-to-end sample](https://github.com/nordfjord/minimal-equinox) covering the key design considerations.
- If you are experienced with CosmosDB and something like [CosmoStore](https://github.com/Dzoukr/CosmoStore), but want to understand what sort of facilities Equinox adds on top of raw event management, see the [Access Strategies guide](https://github.com/jet/equinox/blob/master/DOCUMENTATION.md#access-strategies)

# Design Motivation

Equinox's design is informed by discussions, talks and countless hours of hard and thoughtful work invested into many previous systems, [frameworks](https://github.com/NEventStore), [samples](https://github.com/thinkbeforecoding/FsUno.Prod), [forks of samples](https://github.com/bartelink/FunDomain), the outstanding continuous work of the [EventStore](https://github.com/eventstore) founders and team and the wider [DDD-CQRS-ES](https://groups.google.com/forum/#!forum/dddcqrs) community. It would be unfair to single out even a small number of people despite the immense credit that is due. Some aspects of the implementation are distilled from [`Jet.com` systems dating all the way back to 2013](http://gorodinski.com/blog/2013/02/17/domain-d

[...截断...]

riven-design-with-fsharp-and-eventstore/).

An event sourcing system usually needs to address the following concerns:
1. Storing events with good performance and debugging capabilities
2. Transaction processing
    - Optimistic concurrency (handle loading conflicting events and retrying if another transaction overlaps on the same stream)
    - Folding events into a State, updating as new events are added
3. Decoding events using codecs and formats
4. Framework and application integration
5. Projections and Reactions

Designing something that supports all of these as a single integrated solution results in an inflexible and difficult to use framework. 
Thus, Equinox focuses on two central aspects of event sourcing: items 1 and 2 on the list above. 

Of course, the other concerns can't be ignored; thus, they are supported via other libraries that focus on them:
- [FsCodec](https://github.com/jet/FsCodec) supports encoding and decoding (concern 3)  
- [Propulsion](https://github.com/jet/propulsion) supports projections and reactions (concern 5)

Integration with other frameworks (e.g., Equinox wiring into ASP.NET Core) is something that is intentionally avoided; as you build your application, the nature of how you integrate things will naturally evolve.

We believe the fact Equinox is a library is critical:

  - It gives you the ability to pick your preferred way of supporting your event sourcing system.
  - There's less coupling to worry about as your application evolves over time.

_If you're looking to learn more about and/or discuss Event Sourcing and it's myriad benefits, trade-offs and pitfalls as you apply it to your Domain, look no further than the thriving 4000+ member community on the [DDD-CQRS-ES Discord](https://github.com/ddd-cqrs-es/community); you'll get patient and impartial world class advice 24x7 (there are [#equinox](https://discord.com/channels/514783899440775168/1002635005429825657), [#eventstore](https://discord.com/channels/514783899440775168/762672037113757746) and [#sql-stream-store](https://discord.com/channels/514783899440775168/762671996550774804) channels for questions or feedback)._ ([invite link](https://discord.gg/sEZGSHNNbH))

# Features

- Designed not to invade application code; your domain tests can be written directly against your models.
- Core ideas and features of the library are extracted from ideas and lessons learned from existing production software.
- Test coverage for it's core features. In addition there are baseline and specific tests for each supported storage system and a comprehensive test and benchmarking story
- Pluggable event serialization. All encoding is specified in terms of the [`FsCodec.IEventCodec` contract](https://github.com/jet/FsCodec#IEventCodec). [FsCodec](https://github.com/jet/FsCodec) provides for pluggable encoding of events based on:
  - `NewtonsoftJson.Codec`: a [versionable convention-based approach](https://eiriktsarpalis.wordpress.com/2018/10/30/a-contract-pattern-for-schemaless-datastores/) (using `Typeshape`'s `UnionContractEncoder` under the covers), providing for serializer-agnostic schema evolution with minimal boilerplate
  - `SystemTextJson.Codec`: a replacement to support Microsoft's default serializer - [System.Text.Json](https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=netcore-3.1).  
  - `Box.Codec`: lightweight [non-serializing substitute equivalent to `NewtonsoftJson.Codec` for use in unit and integration tests](https://github.com/jet/FsCodec#boxcodec)
  - `Codec`: an explicitly coded pair of `encode` and `tryDecode` functions for when you need to customize
- Caching using the .NET `MemoryCache` to:
  - Minimize round trips; consistent implementation across stores :pray: [@DSilence](https://github.com/jet/equinox/pull/161)
  - Minimize latency and bandwidth / Request Charges by maintaining the folded state, without needing the Domain Model folded state to be serializable
  - Enable read through caching, coalescing concurrent 