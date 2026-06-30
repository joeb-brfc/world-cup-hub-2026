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

---

# Wireframes

# Wireframes

## Homepage Wireframe

*To be provided.*

---

![Fixtures Wireframe](./static/images/wireframes/fixtures.png)

![Prediction Page Wireframe](./static/images/wireframes/my-predictions.png)

![Pontoon Wireframe](./static/images/wireframes/pontoon.png)

![Prediction Leaderboard Wireframe](./static/images/wireframes/prediction-leaderboard.png)
---

## Mobile Wireframe

*To be provided.*

---

# Relationships

## Current Relationship Testing

The application uses a relational database structure to minimise data duplication and maintain consistency across the platform.

### Team and Fixture Relationships

The `Fixture` model uses foreign key relationships to connect fixtures to teams.

Each fixture has:

* One home team
* One away team

This allows a single team record to be reused across multiple fixtures without duplicating information. For example, Mexico can appear in several fixtures while only existing once within the Team table.

### Fixture and Prediction Relationships

The `Prediction` model uses foreign key relationships to connect users and fixtures.

This means:

* One fixture can have many predictions
* One user can create many predictions

This allows multiple users to predict the same fixture while maintaining individual prediction records.

### User and Pontoon Relationships

The `PontoonBall` model uses a one-to-one relationship with both users and teams.

This ensures:

* One user can only select one Pontoon football
* One football can only be assigned to one user
* One team can only be assigned to one football

These restrictions help maintain fairness within the Pontoon game and prevent duplicate team assignments.

### User and Premium Access Relationships

The `PontoonAccess` model uses a one-to-one relationship with users.

This means:

* One user can have one Pontoon access record
* Each access record belongs to a single user

The relationship is used to control premium access after successful Stripe payment.

## Relationship Testing

Relationships were manually tested through the Django administration panel and application interface.

The following relationships were verified:

* One Team can appear in many Fixtures.
* One Fixture can have many Predictions.
* One User can create many Predictions.
* One User can only select one Pontoon football.
* One Team can only be assigned to one Pontoon football.
* One User can only have one Pontoon access record.
* One User can only participate in Pontoon after access has been granted.

All relationships behaved as expected and enforced the intended business rules.

---

# Features

## Home Page

## Authentication

## Predictor Game

## Prediction Leaderboard

## Pontoon Game

## Pontoon Leaderboard

## Stripe Payments

## Responsive Design

---

# Future Features

- Password reset functionality
- Team fact files
- Expanded World Cup statistics
- Tournament insights
- Additional football competitions
- Improved payment flow with customer details
- Enhanced Pontoon analytics
- Complete webhook-driven access management so Stripe payments update user access without relying on the success redirect.
- Add automatic email confirmations after successful purchases.
- Allow multiple Pontoon competitions to run simultaneously.
- Introduce administrator controls for opening and closing Pontoon competitions.
- Add countdown timers for upcoming fixtures.
- Display live match scores using a football data API.
- Allow users to edit profile information and upload avatars.
- Provide historical leaderboards from previous tournaments.
- Add achievement badges and statistics for prediction accuracy.
- Expand payment options beyond Stripe.
- Improve accessibility further through additional ARIA labels and keyboard navigation enhancements.
- Introduce a dark mode theme.


# Data Model

At this stage of development, the following core models have been created in the `predictor` app:

Fixture
Prediction
PontoonBall
Team
PontoonAccess

These models form the core relational structure of the application.

The `Prediction` model connects authenticated users to fixtures, allowing score predictions to be stored in the database.

## Team Model

- team_name
- group
- flag
- manager
- captain
- best_world_cup_finish
- best_finish_year

## Fixture Model


- home_team
- away_team
- date
- time
- tournament_stage
- home_score
- away_score

## Prediction Model

- user
- fixture
- predicted_home_score
- predicted_away_score
- points_awarded


## PontoonBall Model

Suggested fields:

- number
- team
- selected_by
- score
- busted

## PontoonAccess Model

- user
- has_access
- stripe_pid
- amount_paid
- created_at

---

# Entity Relationship Diagram (ERD)

TO BE PROVIDED

---

# Technologies Used

## Languages

- HTML
- CSS
- JavaScript
- Python

## Frameworks & Libraries

- Django
- Bootstrap 5
- Stripe
- Django Allauth
- Font Awesome
- Google Fonts
- WhiteNoise
- dj-database-url
- PostgreSQL

---

# Code Standards

Code was written following PEP8 guidelines where possible.

---

# Improvements Implemented During Development

## Improvements Implemented During Development

Although the project began with a defined set of user stories, several improvements were identified and implemented throughout development as testing progressed.

### Expanded Fixture Filtering

#### Original Plan

The original fixture page displayed all fixtures together on a single page.

#### Improvement Implemented

As the number of fixtures increased, navigation became more difficult. Matchday filtering was introduced to improve usability.

Users can now filter fixtures by:

* Matchday 1
* Matchday 2
* Matchday 3
* Round of 32
* Round of 16
* Quarter Finals
* Semi Finals
* Final

#### Benefit

This significantly improved navigation and reduced the amount of scrolling required to find fixtures.

---

### Persistent Fixture Filters

#### Original Behaviour

After saving predictions, users were returned to the default fixture page.

#### Improvement Implemented

The application now remembers the user's selected filter and returns them to the same matchday or knockout stage after saving predictions.

#### Benefit

This creates a smoother user experience when entering large numbers of predictions.

---

### Enhanced Payment Confirmation Experience

#### Original Behaviour

After completing a Stripe payment, users were immediately redirected to the Pontoon page with a standard success message.

#### Improvement Implemented

A dedicated payment confirmation page was introduced.

The page now:

* Confirms successful payment.
* Explains that Pontoon access has been unlocked.
* Provides a clear button to continue to the Pontoon game.
* Displays the Stripe payment reference.

#### Benefit

This provides reassurance that payment was successful and creates a more professional user experience.

---

### Improved Pontoon Selection Validation

#### Original Behaviour

Users who had already selected a football could still reach the confirmation screen before being prevented from selecting another team.

#### Improvement Implemented

Validation was moved earlier in the process so users are immediately informed if they have already selected a football.

#### Benefit

This removes unnecessary steps and provides clearer feedback.

---

### Leaderboard Medal System

#### Original Plan

Leaderboards displayed only numerical positions.

#### Improvement Implemented

Gold, Silver and Bronze medals were added for the top three positions.

#### Benefit

This improves visual appeal and makes leaderboard rankings easier to understand.

---

### Authentication Page Redesign

#### Original Behaviour

Login, registration and logout pages used standard Bootstrap card styling.

#### Improvement Implemented

Custom World Cup themed authentication panels were introduced using project branding, custom colours and Font Awesome icons.

#### Benefit

This created a more consistent visual identity throughout the application.

---

### Pontoon Score Visual Indicators

#### Original Behaviour

All positive scores used the same styling.

#### Improvement Implemented

Additional visual feedback was added:

* Gold styling for winning scores.
* Red styling for busted scores.
* Clear status indicators for Winner, Active and Busted teams.

#### Benefit

Users can understand game status more quickly without reading additional information.

### Mobile Hero Button Optimisation

#### Original Behaviour

During responsive testing, the two call-to-action buttons displayed on the homepage hero section were positioned side-by-side on all screen sizes.

Testing revealed that on smaller mobile devices (approximately 400px width and below), the buttons began to overlap, reducing usability and negatively affecting the user experience.

#### Improvement Implemented

A dedicated responsive breakpoint was introduced for smaller mobile devices. Below 420px screen width, the hero buttons automatically stack vertically rather than remaining side-by-side.

#### Benefit

This ensures that users on smaller mobile devices can clearly view and interact with both buttons without overlap or layout issues. The improvement increases accessibility, usability, and overall mobile responsiveness.


---

# Testing

## Manual Testing

### Authentication Testing

| Test | Expected Outcome | Result | Evidence |
|--------|-----------------|---------|---------|
| User can create an account | Account created successfully | Pass | signup.png |
| User can log in with valid credentials | User redirected to application | Pass | login.png |
| Invalid login details | Error displayed to user | Pass | login.png |
| Logged-out user attempts to access predictions | Redirected to login page | Pass | login.png |
| Logged-out user attempts to access Pontoon | Redirected to login page | Pass | login.png |
| User can log out successfully | Session terminated and user logged out | Pass | signout.png |
| Logout confirmation displayed | User prompted before logging out | Pass | signout-confirmation.png |

#### Authentication Screenshots

![Signup](static/images/testing-screenshots/signup.png)

*Figure 1: User registration page.*

![Login](static/images/testing-screenshots/login.png)

*Figure 2: User login page.*

![Logout Confirmation](static/images/testing-screenshots/signout-confirmation.png)

*Figure 3: Logout confirmation page.*

![Logout](static/images/testing-screenshots/signout.png)

*Figure 4: Successful logout process.*

---

### Predictor Testing

| Test | Expected Outcome | Result | Evidence |
|--------|-----------------|---------|---------|
| View all fixtures | Fixtures display correctly | Pass | all-fixtures.png |
| Matchday 1 filter | Only Matchday 1 fixtures displayed | Pass | filteres-fixtures-1.png |
| Matchday 2 filter | Only Matchday 2 fixtures displayed | Pass | filtered-fixtures-2.png |
| Knockout stage filter | Only knockout fixtures displayed | Pass | filtered-fixtures-2.png |
| Save prediction | Prediction saved successfully | Pass | all-fixtures.png |
| Save multiple predictions | Multiple predictions saved successfully | Pass | all-fixtures.png |
| Fixture after kickoff | Prediction automatically locked | Pass | lock-after-kickoff.png |
| Locked fixture | User unable to edit prediction | Pass | lock-after-kickoff.png |
| Competitor predictions visible after kickoff | User can view competitor predictions | Pass | load-competitors-fixtures.png |
| Exact score prediction | 3 points awarded | Pass | predictions-after-two-games.png |
| Correct result prediction | 1 point awarded | Pass | predictions-after-two-games.png |
| Prediction leaderboard updates automatically | Scores recalculated correctly | Pass | predictions-after-two-games.png |
| Gold, Silver and Bronze medals displayed | Top three users awarded medals | Pass | predictions-after-two-games.png |

#### Predictor Test Scenario

After two completed fixtures:

- **joeb** correctly predicted two exact scores and received **6 points**.
- **joe_test1** correctly predicted two match results and received **2 points**.
- **joe_test2** and **joe_test3** received **0 points**.

The leaderboard automatically recalculated and displayed the correct rankings.

#### Predictor Screenshots

![All Fixtures](static/images/testing-screenshots/all-fixtures.png)

*Figure 5: Fixture page displaying available fixtures and prediction inputs.*

![Fixture Filtering](static/images/testing-screenshots/filteres-fixtures-1.png)

*Figure 6: Matchday filtering displaying selected fixtures only.*

![Prediction Locking](static/images/testing-screenshots/lock-after-kickoff.png)

*Figure 7: Locked fixture preventing further prediction changes.*

![Competitor Predictions](static/images/testing-screenshots/load-competitors-fixtures.png)

*Figure 8: Competitor predictions visible after kickoff.*

![Prediction Leaderboard](static/images/testing-screenshots/predictions-after-two-games.png)

*Figure 9: Prediction leaderboard showing automatic scoring and medal rankings.*

---

### Pontoon Testing

| Test | Expected Outcome | Result | Evidence |
|--------|-----------------|---------|---------|
| User accesses Pontoon before selecting a football | Available footballs displayed | Pass | pre-ball-select.png |
| User selects a football | Confirmation page displayed | Pass | pre-ball-select.png |
| User confirms football selection | Football assigned successfully | Pass | post-ball-select.png |
| User attempts to select a second football | Selection prevented | Pass | unable-to-select-second-team.png |
| Assigned team displayed correctly | User's nation and flag shown correctly | Pass | post-ball-select.png |
| Pontoon leaderboard displays participants | Users and scores displayed correctly | Pass | pontoon-after-2-games.png |
| Goals scored increase Pontoon score | Score updates automatically | Pass | pontoon-after-2-games.png |
| Goals conceded reduce Pontoon score | Score updates automatically | Pass | pontoon-after-2-games.png |
| Team reaches exactly 21 points | Winner status awarded | Pass | pontoon-complete.png |
| Team exceeds 21 points | Busted status awarded | Pass | pontoon-complete.png |
| One football per user restriction | Duplicate selection prevented | Pass | unable-to-select-second-team.png |

#### Pontoon Test Scenario

Following multiple completed fixtures:

**Australia**

- Won 2–0
- Won 4–0
- Won 4–0
- Reached exactly **21 points**
- Automatically awarded **Winner** status.

**Morocco**

- Won 4–0
- Won 3–1
- Won 4–0
- Reached **22 points**
- Automatically marked as **Busted**.

The Pontoon leaderboard updated automatically based on goals scored and goals conceded.

#### Pontoon Screenshots

![Pre Ball Selection](static/images/testing-screenshots/pre-ball-select.png)

*Figure 10: Available footballs before a selection has been made.*

![Post Ball Selection](static/images/testing-screenshots/post-ball-select.png)

*Figure 11: Successful football selection and team assignment.*

![Duplicate Selection Prevention](static/images/testing-screenshots/unable-to-select-second-team.png)

*Figure 12: Validation preventing duplicate football selection.*

![Pontoon Leaderboard](static/images/testing-screenshots/pontoon-after-2-games.png)

*Figure 13: Pontoon leaderboard after completed fixtures.*

![Pontoon Completion](static/images/testing-screenshots/pontoon-complete.png)

*Figure 14: Winner and Busted status applied correctly.*

---

### Stripe Payment Testing

| Test | Expected Outcome | Result | Evidence |
|--------|-----------------|---------|---------|
| User without Pontoon access | Redirected to payment page | Pass | pre-payment.png |
| Stripe checkout page loads | Card form displayed correctly | Pass | pre-payment.png |
| Stripe test card accepted | Payment processed successfully | Pass | post-payment.png |
| Successful payment | User redirected to confirmation page | Pass | post-payment.png |
| Pontoon access granted | User gains access successfully | Pass | post-payment.png |
| Existing Pontoon users retain access | Existing users continue to access Pontoon | Pass | post-payment.png |

#### Stripe Screenshots

![Pre Payment](static/images/testing-screenshots/pre-payment.png)

*Figure 15: Stripe checkout page before payment submission.*

![Post Payment](static/images/testing-screenshots/post-payment.png)

*Figure 16: Successful Stripe payment confirmation and Pontoon access granted.*

---

## Responsive Testing

| Device | Result |
|----------|---------|
| Desktop | Layout displayed correctly |
| Tablet | Layout adjusted correctly |
| Mobile | Content remained readable and responsive |

---

## Browser Compatibility Testing

| Browser | Result |
|----------|---------|
| Google Chrome | Pass |
| Microsoft Edge | Pass |
| Mozilla Firefox | Pass |

## Validation Testing

### HTML Validation

![HTML Validation](static/images/testing-screenshots/html-validation.png)

*Figure 11: W3C HTML validation results.*

### CSS Validation

![CSS Validation](static/images/testing-screenshots/css-validation.png)

*Figure 12: W3C CSS validation results.*

### JavaScript Validation

![JavaScript Validation](static/images/testing-screenshots/javascript-validation.png)

*Figure 13: JavaScript validation results.*

### Python Validation

![Python Validation](static/images/testing-screenshots/python-validation.png)

*Figure 14: Python validation results.*

---

## Lighthouse Testing

![Lighthouse Testing](static/images/testing-screenshots/lighthouse-testing.png)

*Figure 15: Lighthouse performance, accessibility, best practices and SEO results.*

## Production Deployment Testing

The application was deployed to Heroku using a PostgreSQL production database. Additional testing was carried out to ensure that functionality worked correctly in both the local development environment and the deployed production environment.

| Test | Expected Outcome | Result |
|--------|-----------------|---------|
| Heroku application deployment | Application deployed successfully | Pass |
| PostgreSQL database connection | Application connected successfully to production database | Pass |
| User registration in production | New users can create accounts | Pass |
| User login in production | Existing users can log in successfully | Pass |
| Fixture data available in production | Fixtures display correctly from PostgreSQL database | Pass |
| Team data available in production | Teams display correctly throughout the application | Pass |
| Pontoon footballs available in production | Footballs display correctly and remain selectable | Pass |
| Existing Pontoon selections retained | Existing users retain assigned footballs and teams | Pass |
| Stripe configuration variables | Stripe checkout loads without configuration errors | Pass |
| Stripe payment processing | Test payments complete successfully | Pass |
| Pontoon access granted after payment | Premium access unlocks correctly after successful payment | Pass |
| Prediction submissions in production | Predictions save successfully to PostgreSQL database | Pass |
| Leaderboard calculations in production | Scores update correctly after fixture results are entered | Pass |
| Prediction locking after kickoff | Fixtures lock automatically once kickoff time has passed | Pass |
| Matchday filtering | Fixtures filter correctly by Matchday 1, 2 and 3 | Pass |
| Knockout stage filtering | Fixtures filter correctly by competition stage | Pass |

### Stripe Payment Testing

Stripe Checkout was implemented to provide paid access to the World Cup Pontoon game.

Testing included:

- Successful payments using Stripe test cards.
- Redirect to the custom payment success page.
- Creation of a `PontoonAccess` record after payment.
- Prevention of unauthorised users accessing the Pontoon game.
- Stripe CLI webhook testing using `stripe listen` and `stripe trigger`.
- Verification that webhook events such as `payment_intent.created`, `payment_intent.succeeded`, `charge.succeeded` and `charge.updated` were successfully received.

The application currently grants Pontoon access through the payment success view after Stripe redirects the user back to the application. Webhook verification has been implemented and tested, with full webhook-driven database updates identified as a future enhancement.

---

### Deployment Challenges Encountered

During deployment several issues were identified and resolved:

- PostgreSQL migration initially resulted in missing production data after switching from SQLite.
- Team, fixture and Pontoon data were re-imported into the production database.
- Existing Pontoon selections required testing after database changes to ensure users retained access.
- Stripe environment variables required configuration through Heroku Config Vars.
- Fixture kickoff times displayed incorrectly after timezone configuration changes.
- Extensive testing was performed using the Heroku shell to compare stored UTC values against displayed UK times.
- Prediction locking behaviour was validated in production to ensure fixtures locked automatically after kickoff.

### Production Deployment Screenshots

#### Heroku Application

![Heroku Deployment](static/images/testing-screenshots/heroku-deployment.png)

*Figure 16: World Cup Hub 2026 successfully deployed on Heroku.*

#### PostgreSQL Database

![PostgreSQL Database](static/images/testing-screenshots/postgresql-database.png)

*Figure 17: Production PostgreSQL database connected successfully.*

#### Production Fixture Locking

![Production Fixture Locking](static/images/testing-screenshots/production-fixture-locking.png)

*Figure 18: Fixture automatically locked after kickoff in production environment.*

#### Production Stripe Payment

![Production Stripe Payment](static/images/testing-screenshots/production-stripe-payment.png)

*Figure 19: Stripe payment system operating successfully in production.*

---

# Screenshots

## Home Page

The Home Page introduces users to World Cup Hub 2026 and provides access to the Predictor and Pontoon games.

![Home Page](documentation/screenshots/home-page.png)

---

## Hero Section

The homepage hero section provides World Cup branding and visual impact using a custom World Cup image.

![Hero Section](documentation/screenshots/hero-section.png)

---

## Fixtures Page

The Fixtures page displays all World Cup fixtures and allows users to submit score predictions.

![Fixtures Page](documentation/screenshots/fixtures-page.png)

---

## Matchday Filtering

Users can filter group stage fixtures by Matchday 1, Matchday 2 and Matchday 3.

![Matchday Filtering](documentation/screenshots/matchday-filtering.png)

---

## Knockout Stage Filtering

Users can filter fixtures by tournament stage including the Round of 32, Round of 16, Quarter Finals, Semi Finals and Final.

![Knockout Stage Filtering](documentation/screenshots/knockout-stage-filtering.png)

---

## Prediction Submission

Users can enter score predictions and save multiple predictions simultaneously.

![Prediction Submission](documentation/screenshots/prediction-submission.png)

---

## Prediction Locked

Once a fixture has kicked off, predictions become locked and can no longer be edited.

![Prediction Locked](documentation/screenshots/prediction-locked.png)

---

## My Predictions

Users can review, edit and delete their saved predictions before fixtures lock.

![My Predictions](documentation/screenshots/my-predictions.png)

---

## Prediction Leaderboard

The leaderboard ranks users based on their total prediction points.

![Prediction Leaderboard](documentation/screenshots/prediction-leaderboard.png)

---

## Login Page

Users can log into existing accounts.

![Login Page](documentation/screenshots/login-page.png)

---

## Sign Up Page

New users can create an account to participate in the games.

![Sign Up Page](documentation/screenshots/sign-up-page.png)

---

## Logout Page

Users can securely log out of their account.

![Logout Page](documentation/screenshots/logout-page.png)

---

## Pontoon Home Page

The Pontoon game allows users to select a football and reveal a randomly assigned World Cup nation.

![Pontoon Home](documentation/screenshots/pontoon-home.png)

---

## Pontoon Team Selection

Users must confirm their football selection before proceeding.

![Pontoon Team Selection](documentation/screenshots/pontoon-confirm-selection.png)

---

## Pontoon Team Display

After selecting a football, users can view their assigned team and current score.

![Pontoon Team Display](documentation/screenshots/pontoon-team-display.png)

---

## Pontoon Leaderboard

The Pontoon leaderboard displays rankings, scores and player status.

![Pontoon Leaderboard](documentation/screenshots/pontoon-leaderboard.png)

---

## Pontoon Payment Page

Users can purchase access to the Pontoon game through Stripe.

![Pontoon Payment](documentation/screenshots/pontoon-payment-page.png)

---

## Admin Panel

The Django administration panel allows fixtures, teams and results to be managed.

![Admin Panel](documentation/screenshots/admin-panel.png)

---

## Mobile Responsive Design

The application has been tested across mobile devices and remains fully responsive.

![Mobile Responsive Design](documentation/screenshots/mobile-responsive-design.png)

---

# Challenges Faced & Solutions

## Initial Database Setup

### Challenge

When attempting to create a Django superuser, an error appeared stating that the `auth_user` table did not exist.

### Solution

The issue was resolved by running:

```bash
python manage.py migrate
```

This created the required Django authentication tables and allowed the superuser account to be created successfully.

### Learning Outcome

This reinforced the importance of running migrations before attempting to use Django models and built-in authentication functionality.

---

## Importing Team Data

### Challenge

The World Cup team data was originally stored in JSON format and could not be imported directly using Django's `loaddata` command.

### Solution

A custom Django shell script was used to create and update team records from the JSON data rather than manually entering all teams through Django Admin.

### Learning Outcome

This demonstrated how custom scripts can simplify large data imports while reducing manual entry errors.

---

## Prediction Authentication Error

### Challenge

During testing, an anonymous user attempted to save a prediction, causing an error because predictions require an authenticated user.

### Solution

The prediction views were protected using Django's built-in authentication decorators.

```python
@login_required
```

### Learning Outcome

This reinforced the importance of securing user-generated content and protecting functionality that requires authentication.

---

## Duplicate Prediction Submission

### Challenge

Submitting a second prediction for the same fixture generated a database integrity error.

### Solution

The prediction logic was updated to use `get_or_create()` so that existing predictions could be updated rather than duplicated.

### Learning Outcome

This demonstrated the importance of enforcing database integrity while maintaining a positive user experience.

---

## Pontoon Team Randomisation

### Challenge

Pontoon footballs were originally assigned alphabetically, making team assignments predictable.

### Solution

Python's built-in randomisation functions were used to shuffle teams before footballs were generated.

```python
import random

teams = list(Team.objects.all())
random.shuffle(teams)
```

### Learning Outcome

This improved fairness and demonstrated how simple Python tools can improve user experience.

---

## PostgreSQL Production Migration

### Challenge

After migrating from SQLite to PostgreSQL on Heroku, the production database contained no fixtures, teams or Pontoon data.

### Solution

The production database was repopulated by importing team, fixture and Pontoon data and validating relationships between models.

The following tasks were completed:

- Restored all 48 World Cup teams.
- Recreated all 48 Pontoon footballs.
- Reloaded World Cup fixture data.
- Verified foreign key relationships.
- Confirmed existing user selections remained intact.

### Learning Outcome

This highlighted the importance of understanding the difference between development and production databases.

---

## Stripe Configuration on Heroku

### Challenge

Stripe payments worked correctly in development but failed on the live Heroku deployment with the error:

```text
No API key provided
```

### Solution

The required Stripe Config Vars were added to Heroku:

```text
STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY
STRIPE_PONTOON_PRICE
```

After deployment, Stripe Elements loaded correctly and payments could be processed successfully.

### Learning Outcome

This reinforced the importance of environment variables and secure production configuration.

---

## Existing User Migration After Payment Integration

### Challenge

After introducing Stripe payments, existing Pontoon players risked losing access because they had no `PontoonAccess` records.

### Solution

A migration script was executed through the Heroku shell to create access records for existing participants.

```python
for ball in PontoonBall.objects.filter(selected_by__isnull=False):
    PontoonAccess.objects.get_or_create(
        user=ball.selected_by,
        defaults={
            "has_access": True,
            "stripe_pid": "manual-free-entry",
            "amount_paid": 0
        }
    )
```

### Learning Outcome

This demonstrated the importance of considering existing users whenever authentication, permission or payment systems are introduced.

---

## Matchday Filtering System

### Challenge

As more fixtures were added to the project, displaying every match on a single page became difficult for users to navigate.

### Solution

A matchday filtering system was introduced using Django URL parameters and queryset filtering.

Users can now view:

- Matchday 1
- Matchday 2
- Matchday 3
- Round of 32
- Round of 16
- Quarter Finals
- Semi Finals
- Final

### Learning Outcome

This demonstrated how Django views and querysets can improve navigation and usability.

---

## Timezone and Prediction Locking Issues

### Challenge

Prediction locking behaved inconsistently between local development and the live Heroku deployment.

Fixtures sometimes remained editable after kickoff or appeared to lock at incorrect times.

### Cause

The issue was caused by timezone differences between Django, Heroku and stored fixture data.

The application initially relied on UTC while users expected fixture times to display in UK time.

### Solution

The timezone configuration was standardised using:

```python
TIME_ZONE = "Europe/London"
USE_TZ = True
```

The prediction locking helper method was then refined:

```python
def predictions_locked(self):
    lock_time = self.kickoff_time + timedelta(minutes=1)
    return timezone.now() >= lock_time
```

Fixture times were validated through Django Admin and the Heroku shell to ensure consistency between stored values and displayed values.

### Learning Outcome

This reinforced the importance of timezone-aware datetimes and production testing when implementing time-sensitive functionality.

---

## User Interface Redesign

### Challenge

The initial interface was functional but lacked a strong football identity and did not fully reflect the World Cup theme.

### Solution

The application was redesigned using:

- Custom CSS variables
- Google Fonts
- Font Awesome icons
- National flags
- Custom buttons and cards
- Responsive layouts
- A World Cup hero image
- Gold, green and purple branding

### Learning Outcome

This demonstrated how visual design choices can significantly improve usability and user engagement.

---

## Hero Image Not Displaying

### Challenge

After implementing the World Cup hero image, the image appeared to be missing despite existing within the static files directory.

### Cause

The browser was serving a cached version of the stylesheet rather than the updated CSS.

### Solution

The static file path was verified and a hard refresh was performed to clear the browser cache.

### Learning Outcome

This highlighted the importance of browser caching when working with static assets.

---

## Duplicate Template Block Error

### Challenge

While updating the fixtures page, Django returned the error:

```text
'block' tag with name 'title' appears more than once
```

### Cause

The template content had accidentally been duplicated, resulting in multiple:

```django
{% block title %}
```

and

```django
{% block content %}
```

sections within the same file.

### Solution

The duplicated code was removed so that only one title block and one content block remained.

### Learning Outcome

This reinforced the importance of carefully reviewing templates when merging large sections of code.

---

## Removing Unused Stadium Functionality

### Challenge

The fixtures page displayed:

```text
Stadium: None
```

for every fixture.

### Cause

Although a Stadium model existed from an earlier design iteration, stadium information was no longer being used within the project.

### Solution

The stadium display was removed from fixture templates.

```html
<p>Stadium: {{ fixture.stadium }}</p>
```

### Learning Outcome

This demonstrated the importance of simplifying applications by removing unused functionality and reducing visual clutter.

---

## Font Integration and Branding

### Challenge

The original typography relied entirely on default Bootstrap styling and lacked a unique visual identity.

### Solution

Google Fonts were introduced:

- Oswald
- Roboto

Font Awesome icons were added throughout the application including:

```html
<i class="fa-solid fa-house"></i>
<i class="fa-solid fa-trophy"></i>
<i class="fa-solid fa-futbol"></i>
```

### Learning Outcome

This demonstrated how third-party resources can improve branding and usability while maintaining responsiveness.

---

