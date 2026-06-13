# Live Application

## Live Link

https://world-cup-hub-2026-861092c83eef.herokuapp.com

---

# Introduction

World Cup Hub 2026 is a Full Stack Django web application based on the FIFA World Cup 2026 tournament. The platform allows users to make score predictions, compete on leaderboards, participate in a World Cup-themed Pontoon game, and explore information about competing nations.

---

# Project Overview

The application combines football predictions, automated scoring, leaderboards, and interactive game features into a single platform. Users can follow tournament fixtures, compare their performance against others, and engage with the competition throughout the World Cup.

---

# Project Purpose

The purpose of the project is to provide football fans with an engaging and interactive way to follow the FIFA World Cup 2026 tournament while demonstrating Full Stack web development skills including:

* Django development
* Relational databases
* CRUD functionality
* User authentication
* Automated scoring systems
* Responsive design

---

# Target Users

The application is aimed at:

* Football fans
* World Cup followers
* Prediction game enthusiasts
* Friends and workplace competitions
* Users interested in football statistics and team information

The platform has been designed to be accessible across desktop, tablet, and mobile devices.


# User Stories

## Home Page

### Visitor User Stories

* As a visitor, I want to understand the purpose of the application immediately so that I can decide whether to register.
* As a visitor, I want clear information about the Predictor and Pontoon games so that I understand how they work.
* As a visitor, I want to see current and planned features so that I know what functionality is available.
* As a visitor, I want a visually appealing football-themed design so that the platform feels engaging and professional.

---

## Authentication

### Registered User Stories

* As a user, I want to create an account so that I can participate in the games.
* As a user, I want to log in securely so that my predictions and Pontoon selections are saved.
* As a user, I want to reset my password if I forget it so that I can regain access to my account.
* As a user, I want restricted areas of the website protected so that only authorised users can access game functionality.

---

## Predictor Game

### Predictor User Stories

* As a user, I want to view all World Cup fixtures so that I can make predictions.
* As a user, I want fixtures organised by stage and matchday so that I can navigate large numbers of games easily.
* As a user, I want to see fixture dates and kickoff times so that I know when predictions close.
* As a user, I want to submit score predictions so that I can compete against other users.
* As a user, I want to save multiple predictions at once so that entering predictions is quick and efficient.
* As a user, I want confirmation that my prediction has been saved so that I know my submission was successful.
* As a user, I want to view my submitted predictions so that I can track my performance.
* As a user, I want to edit or delete predictions before kickoff so that I can change my mind.
* As a user, I want predictions to lock automatically after kickoff so that the competition remains fair.
* As a user, I want to view other users' predictions after a fixture has started so that I can compare my choices with competitors.
* As a user, I want to understand how points are awarded so that scoring is transparent.
* As a user, I want to see my total score so that I can track my position in the competition.
* As a user, I want to see the current leaderboard so that I know who is winning.
* As a user, I want to know how many points separate me from the leader so that I understand what is required to catch up.

---

## Pontoon Game

### Pontoon User Stories

* As a user, I want to see clear instructions explaining how Pontoon works so that I understand the rules before playing.
* As a user, I want to know the scoring system so that I understand how points are earned and lost.
* As a user, I want to see which footballs have already been selected so that I can choose from the remaining options.
* As a user, I want confirmation before selecting a football so that I do not accidentally commit to a team.
* As a user, I want to know that I can only select one football so that the game remains fair.
* As a user, I want my assigned team displayed clearly so that I always know who I am supporting.
* As a user, I want national flags displayed alongside team names so that teams are easy to identify.
* As a user, I want my Pontoon score displayed clearly so that I can monitor my progress.
* As a user, I want to know whether my team is Active or Busted so that I understand my status in the competition.
* As a user, I want to see the Pontoon leaderboard so that I know who is currently winning.
* As a user, I want to see how many points I need to catch the leader so that I understand my chances of winning.

---

## Team Fact Files

### Fact File User Stories

* As a user, I want to browse all competing nations so that I can learn more about the tournament participants.
* As a user, I want to view team managers and captains so that I can learn more about each nation.
* As a user, I want to view each nation's best World Cup performance so that I can compare historical achievements.
* As a user, I want to see national flags so that countries are easy to identify.

---

## Premium Features and Payments

### Premium User Stories

* As a user, I want a secure payment process so that I can purchase premium access safely.
* As a user, I want confirmation that my payment has been successful so that I know premium access has been activated.
* As a user, I want clear information about what premium access includes so that I understand what I am paying for.
* As a user, I want premium functionality restricted to paying users so that the feature retains value.

---

## Administration

### Admin User Stories

* As an administrator, I want to create and manage teams so that tournament information remains accurate.
* As an administrator, I want to create and manage fixtures so that users can make predictions.
* As an administrator, I want to enter fixture results so that prediction scores update automatically.
* As an administrator, I want Pontoon scores to update automatically from fixture results so that standings remain accurate.
* As an administrator, I want teams assigned to Pontoon footballs randomly so that selections remain fair.
* As an administrator, I want only one user to be assigned to each football so that duplicate selections are prevented.
* As an administrator, I want only one team assigned to each football so that teams cannot be duplicated.
* As an administrator, I want users to be marked as Busted when their score exceeds 21 so that Pontoon rules are enforced.
* As an administrator, I want Pontoon scores to support negative values so that goals conceded can reduce scores correctly.
* As an administrator, I want leaderboard positions ordered automatically by score so that the current leader always appears at the top.
