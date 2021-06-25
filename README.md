# Slow Trader

## Project Brief

To create a CRUD application with utilisation of supporting tools,
methodologies and technologies that encapsulate all core modules
covered during training.

## Overview

This project represents the (very) basic structure for a slow paced trading game.
Users own Ships which they use to trade Items with Cities.
Cities are connect by Routes, which Ships move along to travel between Cities. (the state of being in a City will be
represented by a Route that starts and ends in the same city.)

Our MVP is an app that will allow Users to check(read)/update the Ships they own, and command them to move between Cities.
All Users will also be able to "buy"(create) new Ships.
Special Admin Users will be allowed to create and update Cities and Routes.

### Planned Structure

Below is diagram showing the proposed ERD for this project, as well as the "actions" a User will be able to make with their ship. These do not include "book keeping" actions such as renaming ships, or changing user details.

![Imgur](https://i.imgur.com/ar0lEnb.png)

The diagram is split into two sections, the main section is what I want to complete for this project. The section marked "Additional" represents proposed additions to the project for added functionality.

### Risk assessment

The project has been risk assessed and appropriate mitigations have been implemented as shown in the matrix below:
![Imgur](https://i.imgur.com/bxw6t78.png)

The matrix includes assessment of a particular risk's effect, likelihood and severity of occurance and measures to mitigate/control the risk. Finally the effect of the mitigations is evaluated and an estimate of the minimum possible likelihood and severity is given.

### Project management

To manage this project, I made use of a Trello kanban board to track tasks that I needed to complete, as shown below
![Imgur](https://i.imgur.com/K6QoAaM.png)

## Stages of Development
### Stage 1: Users own ships

The first step of the project was to create two tables, Users and Ships, as well as routes and forms as necessary to allow users of the app to create a User, update the details of a User and delete Users, as well as create Ships, rename Ships and delete Ships.

App structure:
![Imgur](https://i.imgur.com/rnmLH9e.png)

### Stage 2: Admin controls

The second development stage invloved creating the infrastructure for the "game map," the Cities for trading in and the Routes for travelling between them. The structure of the new routes is shown below:

![Imgur](https://i.imgur.com/VWEUDFa.png)

### Stage 3: Ships on Routes

Finally the functionality of the relationship between ships and routes was added, allowing the ships to move around the game map. Only one route was added for this stage, "/<ship_id>/sail" which either shows where the ship is sailing to, or allows the user to choose a new destination.

## Testing

Before each stage of development could be considered "complete," comprehensive unit testing was undertaken, each time building on the tests for earlier stages. In this way as new features were added, we could ensure the previous stages still worked correctly, and any errors that came up could be corrected. In this way a high level of coverage was reached at every stage, resulting in ~94% coverage of the final application. The missing 6% is made up of alternative cases of string assignment and rendering html templates, testing these is deemed obsolete owing to the fact that other tests cover their function.

## Using the App

### User Operation

When you starts using the app, you will be greeted by a list of other Users and a "Create a new eser" option. Following this link takes you to a form where you can enter a username and email address to create your user. With this done, you can now click you username in the list, where you will be taken to your ship list. Alternatively there are options to update your details or delete your account (WARNING deleting your account is done without confirmation)

From your ship list, you can either select a ship, or build a new one. Building a new ship simply requires naming it, choosing a type, fast, medium or slow and choosing a city to build it in.

If you select a ship, you are given options for renaming the ship or deleting it. Most importantly is the option to "Sail" this will allow you to move your ship to a different city, provided there is a route between them.


