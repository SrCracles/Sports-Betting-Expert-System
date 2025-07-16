[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/irotxg5d)

# Sports Betting Expert System

## Team Members

- **Alejandro Mejía**
- **Julio Prado**
- **Angel Ordoñez**

## Description

This project implements a medium-complexity expert system to assist users in making informed decisions in sports betting for World Cup matches. The system combines rule-based reasoning with Bayesian inference to classify betting scenarios as "safe" or "risky", providing well-founded recommendations.

## Main Features

- **Hybrid Reasoning**: Combines symbolic rules (Experta) with probabilistic reasoning (pgmpy)
- **User Interface**: Interactive Telegram bot for data collection
- **Comprehensive Analysis**: Evaluates multiple factors such as team performance, injuries, weather conditions, match importance
- **Explanations**: Provides clear justifications for each recommendation
- **Robust Validation**: Comprehensive test suite with historical data

## Usage

First run the bot locally:
```bash
python src/bot.py
```

Interact with the Telegram bot by searching for: **@futifu_bot**


## System Features

The system evaluates multiple variables to generate recommendations:

- **Team Data**: Performance, goals scored/conceded, win percentage
- **Contextual Factors**: Weather conditions, crowd support, match importance
- **Historical Analysis**: Results from previous encounters
- **Risk Assessment**: Key player injuries, result streaks

### Recommendation Types

- **home_win**: Bet on home team victory
- **away_win**: Bet on away team victory
- **draw**: Bet on draw
- **avoid_bet**: Avoid betting (high-risk scenario)

## Testing

The system includes comprehensive tests that validate:

- **Historical Accuracy**: Comparison with real match results
- **Expert Validation**: Agreement with specialist predictions
- **Usability**: Response time and interpretability
- **Robustness**: Handling of edge cases and concurrent processing


