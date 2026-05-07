Please help with verifying or updating older sections of this article.At least some were last verified forversion1.30.

Thescoring systemin Europa Universalis IV ranks countries by their successes in theadministrative,diplomaticandmilitarycomponents of the game.

### Contents

- 1Gaining score
- 2Rating2.1Administrative rating2.2Diplomatic rating2.3Military rating
- 2.1Administrative rating
- 2.2Diplomatic rating
- 2.3Military rating
- 3Score modifiers3.1Difficulty3.2Increase over time3.3Bonus3.4Penalty3.5Typical scenarios3.6Hegemons
- 3.1Difficulty
- 3.2Increase over time
- 3.3Bonus
- 3.4Penalty
- 3.5Typical scenarios
- 3.6Hegemons
- 4Victory cards4.1How to Disable Victory Cards:4.1.1Disable in Options:4.1.2Editing a Save File(for an ongoing game):
- 4.1How to Disable Victory Cards:4.1.1Disable in Options:4.1.2Editing a Save File(for an ongoing game):
- 4.1.1Disable in Options:
- 4.1.2Editing a Save File(for an ongoing game):
### Gaining score[edit|edit source]

The top ten nations in each of the three categories earn points towards their overall score at the end of every month. The point values vary based on the nation's ranking in each category with higher ranks earning more. A nation cannot lose points, and there are no penalties for falling behind, but if a nation is outside the top ten, then it will not get any points that month. Additionally victory cards grant score.

### Rating[edit|edit source]

Ranking is determined by the following ratings:

#### Administrative rating[edit|edit source]

Administrative rating assesseseconomic, political and bureaucraticaspects of a country.

Losing wars:-0.25xtotal administrative rating for 5 years.

(This increases the administrative rating when it is negative)

Winning wars:+0.25xtotal administrative rating for 5 years.

(This decreases the administrative rating when it is negative)

(The modifiers stacks according to the order of peace deals)

#### Diplomatic rating[edit|edit source]

Diplomatic rating considers a country'sinternational relations and naval power.

+0.03333333333 per trade ship

+0.066666666666 per galley

+0.02 per transport

Losing wars:-0.25xtotal diplomatic rating for 5 years.

(This increases the diplomatic rating when it is negative)

Winning wars:+0.25xtotal diplomatic rating for 5 years.

(This decreases the diplomatic rating when it is negative)

(The modifiers stacks according to the order of peace deals)

#### Military rating[edit|edit source]

Military rating evaluates theland warfare capabilitiesof a country.

Losing wars:-0.25xtotal military rating for 5 years.

(This increases the military rating when it is negative)

Winning wars:+0.25xtotal military rating for 5 years.

(This decreases the military rating when it is negative)

(The modifiers stacks according to the order of peace deals)

### Score modifiers[edit|edit source]

#### Difficulty[edit|edit source]

#### Increase over time[edit|edit source]

The score gains increases as the game progresses to later dates. The modifier changes from-75%score gain per month on 1444 to+406.21%score gain per month by 1821.

#### Bonus[edit|edit source]

- Sufficient rivals/No possible rivals:+10%score gain per month. This bonus applies to all three categories.
- Stronger rival:+10%per each rival whose rank is higher than the country. Counted separately for each category. Stack with rival not enough penalty. Do not stack with default+10%bonus.
#### Penalty[edit|edit source]

- Not enough rivals:-25%per each empty rival slot. This penalty applies to all three categories.
#### Typical scenarios[edit|edit source]

#### Hegemons[edit|edit source]

The Hegemony system introduced inEmperor expansionsystem also grants a 2% bonus to final score earned per month for allhegemons.

### Victory cards[edit|edit source]

In multiplayer, countries at 300developmentor more will get victory cards every 100 years from 1450 and onwards, to a total of 4 cards at 1750. A victory card requires a nation to own, control andcorea certainarea. The cards are randomly picked near the nation (player) or its subjects where the areas belong to potential or current rivals. There is a higher chance of getting the cards on nations ahead in score or belonging to other players.

The first victory card is worth 1000 points with each subsequent card worth +1000 than the one before. The score then ticks upwards over the course of 10 years up to the card's maximum value. If the area of the card is lost the score will begin ticking downwards until it reaches zero (again, over a period of 10 years). A completed victory card is worth +1 score per month.

Victory cards owned by opponents on previously controlled provinces reduce score by 50% of their value.

#### How to Disable Victory Cards:[edit|edit source]

##### Disable in Options:[edit|edit source]

- Before starting a game, you can simply disable victory cards in the game options.
##### Editing a Save File(for an ongoing game):[edit|edit source]

If your game is already in progress, you’ll need to edit the save file to disable victory cards.

1.Steps:

- Make a backupof your save file before editing. (If you are not sure how to do it.)
- Open the save file using a text editor.
- PressCtrl + Fand search forgameplaysettings.
2.Disable Victory Cards:

- Locate the 21st digit undersetgameplayoptions.
- Change that digit to0to disable victory cards from spawning (if they’re enabled, it will be set to1).
3.Identify Your Nation:

To remove existing victory cards, you need to identify your nation in the save file. Since your nation isn’t named directly, use the rival IDs to locate your country.

- UseCtrl + Fand search forival={
   country="RIVAL_ID"
```
rival={
   country="RIVAL_ID"
```

Replace"RIVAL_ID"with the tag ID of one of your nation's rivals to find your nation's section.

4.Remove Victory Cards:

- Once you’ve found your nation, search for and delete eachvictory_cardentry associated with your nation. It will look like this:victory_card={
   area="example_area"
   level=1
   score=0.000
   was_fulfilled=no
}
```
victory_card={
   area="example_area"
   level=1
   score=0.000
   was_fulfilled=no
}
```
