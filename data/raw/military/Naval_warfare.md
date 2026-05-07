Please help with verifying or updating older sections of this article.At least some were last verified forversion1.25.

Naval warfareis the competition of sea-going power between nations at war. While a majority of warfare is land-based, the naval aspect of conflict can be incredibly influential in the spheres of trade, colonisation and conquest.

### Contents

- 1Sea battle interface
- 2Engagement width
- 3Combat sequence3.1Engagement3.2Phases3.3Target selection3.4Die roll3.5Hull damage3.6Morale damage3.7Disengagement
- 3.1Engagement
- 3.2Phases
- 3.3Target selection
- 3.4Die roll
- 3.5Hull damage
- 3.6Morale damage
- 3.7Disengagement
- 4Combat statistics4.1Cumulative diplomacy technology effects to navy4.2Cumulative military technology effects to navy4.3Max naval morale4.4Combat ability4.5Unit pips4.6Leader pips4.7Concluding a battle
- 4.1Cumulative diplomacy technology effects to navy
- 4.2Cumulative military technology effects to navy
- 4.3Max naval morale
- 4.4Combat ability
- 4.5Unit pips
- 4.6Leader pips
- 4.7Concluding a battle
- 5Morale and strength5.1Morale5.2Morale recovery5.3Unit strength5.4Ship repair
- 5.1Morale
- 5.2Morale recovery
- 5.3Unit strength
- 5.4Ship repair
- 6Fleet actions6.1Start patrolling6.2Coastal Raiding6.2.1Mechanism6.2.2"May raid coasts" ability6.3Blockading6.3.1Blockade power6.3.1.1Blockade efficiency6.3.1.2Blockade force required6.3.2Effects of blockade6.4Blocking a strait
- 6.1Start patrolling
- 6.2Coastal Raiding6.2.1Mechanism6.2.2"May raid coasts" ability
- 6.2.1Mechanism
- 6.2.2"May raid coasts" ability
- 6.3Blockading6.3.1Blockade power6.3.1.1Blockade efficiency6.3.1.2Blockade force required6.3.2Effects of blockade
- 6.3.1Blockade power6.3.1.1Blockade efficiency6.3.1.2Blockade force required
- 6.3.1.1Blockade efficiency
- 6.3.1.2Blockade force required
- 6.3.2Effects of blockade
- 6.4Blocking a strait
- 7Naval missions7.1Protect trade7.2Privateer7.2.1Privateer efficiency7.2.2Range7.2.3Effects7.3Hunt pirates7.4Explore7.5Hunt enemy fleet7.6Blockade enemy ports7.7Intercept enemy fleets
- 7.1Protect trade
- 7.2Privateer7.2.1Privateer efficiency7.2.2Range7.2.3Effects
- 7.2.1Privateer efficiency
- 7.2.2Range
- 7.2.3Effects
- 7.3Hunt pirates
- 7.4Explore
- 7.5Hunt enemy fleet
- 7.6Blockade enemy ports
- 7.7Intercept enemy fleets
- 8Strategies and tactics8.1Deployment8.2Bringing an enemy fleet to battle
- 8.1Deployment
- 8.2Bringing an enemy fleet to battle
- 9Footnotes
### Sea battle interface[edit|edit source]

Likeland warfare, naval combat occurs when opposingfleetsconfront each other in the same seaprovince. Also like land battles, these sea battles can go on for many days, so they should be considered not as a single engagement, but as two fleets maneuvering to gain wind, standing off and skirmishing before the fleets finally collide.

In EU4, there is no player involvement inside combat, but the interface now displays more information, showing among other information which ship is fighting which.
The naval combat interface shows the strength of the two fleets engaged in the combat. Combat will begin with a contest of firepower, followed by shock action in which ships attempt to grapple or ram one another. This sequence will alternate until one of the fleets loses morale and is either routed or destroyed. The condition of each ship (being the number of sailors still alive on that ship to fight) is expressed as a percentage, and hovering over a ship with the mouse cursor will produce a tooltip which identifies which opposing ship they are currently firing on, as well as their current morale, their strength, and the ship type.

### Engagement width[edit|edit source]

Engagement width is the combat width for naval battles. Unlike thecombat widthof land warfare, the naval engagement width of the two participants are independent, that means one participant could have wider engagement width than the other. Heavy ships occupy 3 combat width, while galleys, transports and light ships each occupy 1 combat width.[1]

Engagement width has a base of 5.[2]It increases over time as diplomatic technology improves.

Though not mentioned anywhere in the game, modifiers to the engagement width are separated into two categories, global modifiers and local modifiers. When these modifiers are applied to the base engagement width, it is done according to this formula:

Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle EngagementWidth = BaseEngagementWidth \cdot GlobalModifiers \cdot LocalModifiers}

Global modifiers can be gained from following:

- Piratical idea 4: Sail in Consort
- Naval-Exploration: Skilled Cartographers
- Danish ambition
- Maritime idea 6: Seahawks
- Naval idea 7: Superior Seamanship
- Naval-Espionage: The Maritime Intelligencer Unit
And the following modifiers count as local modifiers:

Aflagshipwith“Improved Crow's Nest” modification increases the fleet engagement width by+3. It should however be noted that this increase is only applied once (stacking flagships with said modification do not further increase it) and is applied AFTER other engagement width modifiers, it is therefore always just a flat+3to the engagement width.

### Combat sequence[edit|edit source]

Like land warfare, naval combat occurs when opposing fleets confront each other in the same sea province. Also like land battles, these sea battles can go on for many days, so they should be considered not as a single engagement, but as two fleets maneuvering to gain wind, standing off and skirmishing . A sea battle will last until one side is routed or annihilated. Patch 1.16 also introduced the concept of a naval combat width, and much like its land cousin it is the total number of ships that can engage the enemy at any one time.

#### Engagement[edit|edit source]

While there is an ongoing naval battle, fleet's ship will try to populate its engagement width until the limit is reached, in the following order:

1. Heavy ships
1. Galleys
1. Light ships
1. Transports
Any ships already disengaged will be ignored, and galleys gain priority over heavy ships when battling in inland seas.

Importantly, any ships in excess of the engagement width are placed in reserve (until they replace those destroyed or disengaged) where they suffer morale damage although not in the fight. Therefore be sure to rather time adding smaller fresh and high morale reinforcements during each phase of the battle than merely throwing one full stack at the enemy.

#### Phases[edit|edit source]

Combat is divided into a series of 3-day phases where the phases alternate between fire and shock, with the fire phase happening first. Therefore each 6 days (after a full cycle of fire and shock) it may be best to try and reinforce the engagement width line with fresh reinforcements as others have been lost or disengaged during these two phases. Staying in reserve in the backline causes severe morale reductions, even while not fighting. So timing reinforcements to match the phases is generally better than depending on ships in reserve.

#### Target selection[edit|edit source]

Targeting, and specifically combined targeting, is why the "cannon:hull strength" ratio together with the relative combat width is so important in determining the outcome of a naval battle.

In combat each ship in the front line (all ships up to the engagement width) will try to find a target and make an attack. Every enemy ship has a base chance of 10 to be picked as a target, further modified by:

- +0 to +5 random chance
- +5 if same type (hence heavies are more likely to target other heavies, and galleys to target other galleys)
- x0.1 if morale at 0 or less
- x2 if hull strength is less than 50% (hence their appeal is doubled, resulting in many ships focusing fire or "ganging up" on the same weaker targets)
The enemy ship with the highest score is selected as a target. If the previous target is about to die, a new one will be targeted. This group focus on the weaker ones below 50% to push them to zero is why a battle can so quickly turn; normally as one runs out of reinforcements or ships in reserve and those still remaining in the fight have their morale collapseen masse.

Note that unless a ship disengages it may remain in the combat width line-up at near zero value, inhibiting a fresher high-strength ship to replace it in the combat width. This makes increases in disengagement chances very valuable.

The successful outcome of this combined targeting can be enhanced by your maximizing the number of cannons to target (from sending in higher quality ships - whether heavies or galleys, and from having a disproportionately higher engagement width than the enemy) as Cannons/Target Hull is the key factor in both the Final Damage and Morale Loss calculations.

#### Die roll[edit|edit source]

At the beginning of each phase, each side rolls a die. The result is used to determine the morale damage and hull damage inflicted by that side during each of the three days of that phase. Some ideas and the wooden wall naval doctrines give a bonus to the die roll when fighting off an owned coast.

- Barbary Corsair idea 3: Vengeful Refugees
- Eora idea 5: The Sacred Shore
- Malayan idea 4: Chart the Isles
- Norse idea 2: Norse Seamen
- Piratical idea 6: Pirate Bays
#### Hull damage[edit|edit source]

Base damage is calculated according to the following formula:

Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle Base Hull Damage = 0.025 + 0.025 \cdot (2 + Dice + Combat Modifiers)},

where Combat Modifiers include the Artillery Fire Modifier, Naval Doctrine Bonus (England) and Admiral pip value difference (between 0 to 6) for that phase of the battle. Ship Combat Ability and Admiral Combat Ability are modifiers applied in the Final Damage formula.

The amount of cannons of the attacking vessel affects the hull damage dealt and the hull strength (hull size) of the defender decides how long it can stand the cannon fire.

TheArtillery Fire Modifiergives a bonus or penalty to damage dealt depending on if attacker or defender has a technological advantage (with referencenotto its Diplomatic Tech, but rather to its Military Tech, and therefore to the relative difference between each side's artillery damage modifiers). For example, jumping from tech 21 to tech 22 relative to your enemy in fact means a cumulative artillery fire difference of+2(+4.4 vs. +2.4), which doubles this modifier.

- Attacking unit modifier: The attack modifier from the attacking unit's technology, i.e. "Artillery Fire".
Artillery Fire Modifier = Attacker Artillery Fire - Target Artillery Fire

- Attacking unit Combat Ability: Any Combat Ability bonuses the attacking unit has.
Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle Final Damage = 0.03 \cdot Base Hull Damage  \cdot  Ship Strength  \cdot  \frac{Cannons }{ Target Hull}  \cdot  (1 + 0.05  \cdot  Artillery Fire Modifier)  \cdot  \frac{1 + Ship Combat Ability + Combat Ability from Admiral}{1 + Target Ship Durability}}

If target ship Morale is 0 or below, Final Damage is multiplied by 10.

Importantly, note that since Ship Durability is the denominator (and therefore affecting all the factors), one can drastically reduce the damage taken by having any modifiers that increase durability. For example, the 5% from the Corvettes Idea under Quality.

Galleys fighting in the inland sea have their Final Damage doubled. Which means that in inland seas, instead of fighting 3 galleys, one heavy is effectively fighting 6. Hence it's best to match galleys to galleys in inland seas and try and maximise your engagement width using a high pip manoeuvre admiral. Having a naval reformer advisor to boost morale will help too.

#### Morale damage[edit|edit source]

Morale is damaged both over time during a battle and also when a friendly ship is sunk.

Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle Base Morale Damage = 0.25 \cdot \frac{Country Naval Morale}{3} \cdot Base Hull Damage \cdot Ship Strength \cdot \frac{Cannons}{Target Hull} \cdot (1 + 0.05 \cdot Artillery Fire Modifier) \cdot (1 + Ship Combat Ability + Combat Ability from Admiral)}

Several ideas decrease the amount of morale lost when a ship is sunk:

- Naval idea 3: Naval Cadets
- Humanist-Maritime: The Citrus Statute
- Betsimisaraka traditions
- Galician idea 6: Sailors of the Cantabrian Sea
- Naxian idea 2: Naxos Rules The Waves
- Sulu idea 5: Dagat Sulu
- Catalan ambition
- Exploration-Defensive: The Naval Secrecy Act
- Naval-Religious: Zealous Captains
#### Disengagement[edit|edit source]

Any ship with less than 0.5 morale will try to disengage from the battle. Whether it will be successful depends on the ship's Disengagement Chance. The base value of this chance is 10% but can be modified by some national ideas.

- Indigenous-Maritime: Canoe Expertise
- Fully Naval
- Australian idea 5: Royal Australian Navy
### Combat statistics[edit|edit source]

#### Cumulative diplomacy technology effects to navy[edit|edit source]

#### Cumulative military technology effects to navy[edit|edit source]

note : ONLY the Artillery Fire difference between attacker and defender is calculated, not the total, so the +1 of Spain and Aragon mean they have ALWAYS an impact (5% hull damage) if on time in naval tech.

#### Max naval morale[edit|edit source]

The following contributes to the maximum morale of a nation's navy.

Certain National Ideas, Idea groups and policies will bump naval morale.

- Alaskan traditions
- British traditions
- Genoese idea 2: The Lessons of Chioggia
- Kono idea 3: Oyamazumi Shrine
- Livonian idea 6: Naval Professionalism
- Norwegian idea 3: Natural Seamanship
- Scandinavian idea 4: Norwegian Marines
- So idea 3: Fight for Tsushima
- Luzon ambition
- Omani traditions
- Acehnese/Pasai idea 4: Military Adventures
- Bregenzer idea 7: The Lake Constance Navy
- Bruneian idea 6: Naval Prowess
- Chiba idea 7: Naval Reform
- Corsican idea 2: The Battle of Meloria
- Danish idea 5: Naval Heroes
- Eora idea 1: Eora Lifestyle
- Madyas idea 2: Legacy of Panai
- Malayan idea 4: Chart the Isles
- Manx idea 4: Mann and the Isles
- Navarran idea 1: Fearless Seamen
- Norse idea 2: Norse Seamen
- Ouchi idea 3: Protect Against Piracy
- Sicilian idea 6: The Grand Navy
- Anglo-Dutch ambition
- Dalmatian ambition
- Mogadishan ambition
- Ragusan ambition
- Siddi ambition
- Candarid traditions
- Naval idea 7: Superior Seamanship
- Quality idea 5: Naval Drill
- Eastern Algonquian idea 5: Whale Hunters
- Piratical idea 5: Elected Quartermasters
- Portuguese idea 1: Legacy of the Navigator
- English ambition
- Exploration-Defensive: The Naval Secrecy Act
- Quality-Maritime: The Organized Marines Act
- Religious-Maritime: Chaplains of the Fleet
- Korean idea 6: Geobukseon
Each point of naval tradition also increases naval morale recovery by+0.10%.

#### Combat ability[edit|edit source]

Combat abilityis a value that is multiplied with the units' damage dealt (both for casualties and morale),  but only for the specified type of unit.

Heavy ship combat ability improvement

- Naval idea 6: Oak Forests for Ships
- British traditions
- Butuan idea 6: Protect the Coastlines
- Date idea 5: Red Seal Ships
- English idea 1: A Royal Navy
- Lübeckian (Hansa) idea 4: Adler von Lübeck
- Majapahit idea 6: The Majapahit Armada
- Spanish idea 4: A Spanish Armada
- Alaskan ambition
- Genevan ambition
- Innovative-Maritime: New Naval Tactics
+10%Heavy ship combat ability from Mamluk Warships Naval Doctrine.

+5%Heavy ship combat ability from Atakebune Naval Doctrine.

Light ship combat ability improvement

- Veronese ambition
- Hawaiian traditions
- Alaskan traditions
- Cham traditions
- Eora traditions
- Ferraran traditions
- Icelandic idea 4: Armed Merchants
- Moluccan idea 6: Alliance with the Papuans
- Arakanese ambition
- Holstein ambition
- Fijian traditions
- Hamburger traditions
- Pattani traditions
- Somali idea 6: Corsairs of the Red Sea
- Sumatran idea 3: Spice Pirates
Galley combat ability improvement

- Most Serene traditions
- Naval idea 2: Improved Rams
- Malayan idea 2: Advanced Galley Warfare
- Venetian (upgraded) ambition
- Venetian ambition
- Aragonese traditions
- Barbary Corsair traditions
- Cebu traditions
- Hosokawa traditions
- Ionian traditions
- Tunisian traditions
- Berber idea 7: The Brothers Barbarossa
- Bruneian idea 1: Galley Fleet
- Cypriot idea 6: Repel the Corsairs
- Italian idea 3: Mare Nostrum
- Kitabatake idea 4: Kuki Suigin
- Knights Hospitaller idea 4: Reconquista of the Sea
- Moroccan idea 4: Defend the Coastline
- Kono idea 5: Rule Over the Inland Sea
- Somalian ambitions
- Maritime-Quantity: Streamlined Galley Production
- Latin idea 4: Trading Guilds of Pera
- Naxian idea 1: Maritime State
- So idea 2: Wakou Tradition
+20%Galley combat ability from Tactica Naval Doctrine.

+15%Galley combat ability from Mamluk Galleys Naval Doctrine.

+15%Galley combat ability from Free Oarsmen Naval Doctrine.

#### Unit pips[edit|edit source]

Each ship has stats in three categories:Hull,Cannon, andSpeed.

Hull is the defensive stat, and cannons the offensive stat. With the exception of Morale, every combat phase the hull/cannon pips are used against each other to calculate the number of hull damage of each combat phase. Therefore, the damage sustained by the hull is directly proportional to the number of cannons firing at it.

#### Leader pips[edit|edit source]

Leaders are rated on a scale of 0 to 6 for each of the following skills:

- Fire,Shock
The leader's skill difference is added to the dice roll of its respective phases.

- Dutch idea 4: Instructie voor de Admiraliteiten
- United Crowns idea 3: Instructie voor de Admiraliteiten
- Naval idea 3: Naval Cadets
- Ferraran idea 7: The Ferraran Arsenal
- Norman idea 7: Great Commanders
- Tunisian idea 5: Board of Captains
- Corsican ambition
- Madyas ambition
- Navarran ambition
- Court-Naval: Naval Competence Act
- Naval-Innovative: The Nautical Education Act
- Naval idea 1: Boarding Parties
- Danish idea 5: Naval Heroes
- Madyas idea 4: Masters of Maritime Warfare
- Norse idea 3: A Wall of Shields for the King
- Naval-Religious: Zealous Captains
- Maneuver
The leader's maneuver affects the movement speed of the fleet both on the map and in battle. Each point also grants 5% additional trade power when assigned to a fleetprotecting tradein a trade node. Finally, it reduces attrition taken by 1% per skill level.

- Madyas traditions
- British idea 7: Britannia Rules the Waves
- Hawaiian idea 7: Legendary Voyagers
- Mahri idea 4: Pilots of the Arabian Sea
- Mogadishan idea 2: Somali sailors
- Omani idea 6: Skilled Captains
- Somalian idea 4: Zeila and Berbera
- Swahili idea 2: Monsoon Season
- Court-Naval: Naval Competence Act
- Innovative-Maritime: New Naval Tactics
- Maritime-Offensive: Hold the Weather Gauge
#### Concluding a battle[edit|edit source]

A naval battle ends when one side is either:

- Reduced to 0 morale;or
- Flees from combat;or
- Annihilated (stack wiped)
Upon victory, ships from the defeated fleet may be captured, depending on your chance to "capture enemy ship" (during a battle, hover your cursor over this percentage in the top right of the battle popup). Your capture chance is affected by selecting "ship boarding" as your naval doctrine (providing you a 33% chance of capturing a ship), ideas such as the "reconquista of the sea" of The Knights (15% chance), policies from Naval&Diplomatic (33%), and the relative maneuver skill difference between the admirals of the two fleets. Generally very few or no ships will be captured for leaderless (0 vs. 0 maneuver) battles.

If the defeated fleet still has ships remaining, it will escape to the nearest friendly port to repair and recover its morale. Naval battles, like land battles, may causewar exhaustionas well as affectwarscore,naval traditionandprestige. Note that warscore gained from naval battles will generally be insignificant compared to those gained by its land counterparts.

In the event that more than one nation is on the winning side of a battle, thelargest fleeton that side will receive any captured ships.

Several ideas increase the chance of capturing ships after a battle:

- Naval-Diplomatic: Terms of Surrender Statute
- Espionage idea 6: Privateers
- Offensive-Exploration: Sponsored Privateers
- Betsimisaraka idea 5: European Pirate Communities
- Knights Hospitaller idea 4: Reconquista of the Sea
- Cornish idea 4: Pirates of Penzance
- Dithmarscher idea 4: Expert Wreckers
- Kono idea 7: Murakami Suigun
- Pattani idea 4: Lian Dao-Qian Band
### Morale and strength[edit|edit source]

#### Morale[edit|edit source]

Morale is an important factor in fighting battles. Each turn of combat a unit will take a Morale hit. Once a fleet's average Morale value has been reduced to zero the fleet will attempt to retreat. Retreat cannot happen until both a fire and a shock phase have completed, so a fleet that has its morale reduced to 0 before that point will be destroyed.

If a fleet loses a battle while having low enough morale, they will be forced to retreat to a port of the nearest sea province. While retreating, it cannot be engaged in combat or be controlled until it reaches the sea province, nor will it repair.  The fleet will also move 50% faster, and will recover morale at a normal rate during the retreat.

After every battle is fought a fleet must spend some time not fighting for its morale to recover.

#### Morale recovery[edit|edit source]

Every month when docked at a home port, a ship recovers a 10% of its maximum morale.

Certain National Ideas, Idea groups and policies will increase naval morale recovery.

- Palembang idea 6: Through the Monsoon
- Naval-Innovative: The Nautical Education Act
- Humanist-Naval: The Naval Inspection Act
- Religious-Maritime: Chaplains of the Fleet
Each point of naval tradition also increases naval morale recovery by+0.1%.

#### Unit strength[edit|edit source]

Unit strength is an important factor in fighting sea battles. Naval unit strength affects how long it can stand cannon fire before sinking. Each turn of combat a unit will take hull damage reducing its strength.

Galleys gain a bonus of 100% strength in inland seas[3]and a bonus of 50% strength in coastal sea tiles which are not in inland seas[4]. The inland seas are shown below in pale blue, the coastal seas in blue and open seas in dark blue.

#### Ship repair[edit|edit source]

Fleets that have sustained damage will automatically repair up to their full strength when docked in an owned, allied, or in a province with fleet basing rights. There is a 'repair damaged' button that will detach damaged ships and send them to a nearby port to repair, when they are back up to full strength they will rejoin the fleet.

### Fleet actions[edit|edit source]

#### Start patrolling[edit|edit source]

Thestart patrollingbutton orders a fleet to loop its current movement order: when it reaches the final destination of its current set of movement orders, it will automatically head back to the point where the patrol was started. Patrol routes can include port visits, where the patrol stops until all ships are repaired.  While the same function can be fulfilled by light ships assigned to protecting trade nearby, patrols are not limited by ship type, trade power, or trade range.

#### Coastal Raiding[edit|edit source]

Coastal Raiding is a naval ability which allows fleets belonging to nations with the Raid Coasts idea to raid the coasts of other nations forloot (ducats) andsailors.

Historically, this ability reflects the raids carried out by Barbary pirates which were active in the Mediterranean Sea during the mid-16th to early 19th centuries while in the case of the three Pirate Republics, it simulates the Golden Age of Piracy in the Caribbean Sea from the mid-16th to the early 18th century.Sois a special case, as it represents a resurgence of the Japanese Wokou Pirates that raided the coasts of East Asia intermittently from the 4th century to the 17th century.

Raiding can provide a significant early-game boost to the income and sailor pools of nations that can do it and can also serve as a way to damage the economy of other nations. An example of this isSo, which can employ Coastal Raiding againstMingto pile up devastation and cause Ming to potentially lose theMandate of Heavenand collapse.

##### Mechanism[edit|edit source]

A fleet can raid a coastal province if all of the following is true:

- The raiding nation “may raid coasts” (seebelow).
- The raider must be able to place a fleet in a sea tile adjacent to the province (but doesn't need to be able toblockade the port).
- The target province fulfills all the following conditions:Is no more than three sea tiles away from a province owned by the raiding nation. This can be increased with the modifier“Coastal raiding range”present in the 2ndPiratical idea).Has adevelopment lower than or equal to theblockading powerof the raiding fleet.Isnotowned by a country which has a truce with the raiding nation.Isnotof thereligionof the raiding nation or belongs to a country with the same religion as the raiding nation (unless the contrary is specified by the“May raid coasts including coasts of countries with same religion”ability).Isnotcontrolled by a “friend” (subject, overlord, subject of the overlord, ally, subject of ally, in the same trade league, country with above 100 opinion) of the raiding nation.Hasnotthe“Raided Coast”modifier.
- Is no more than three sea tiles away from a province owned by the raiding nation. This can be increased with the modifier“Coastal raiding range”present in the 2ndPiratical idea).
- Has adevelopment lower than or equal to theblockading powerof the raiding fleet.
- Isnotowned by a country which has a truce with the raiding nation.
- Isnotof thereligionof the raiding nation or belongs to a country with the same religion as the raiding nation (unless the contrary is specified by the“May raid coasts including coasts of countries with same religion”ability).
- Isnotcontrolled by a “friend” (subject, overlord, subject of the overlord, ally, subject of ally, in the same trade league, country with above 100 opinion) of the raiding nation.
- Hasnotthe“Raided Coast”modifier.
When a coast is raided, the loot provided is the sum of the available loot of the provinces eligible for raid, as follows:

- As muchducats as available loot (i.e.development affected byavailable loot modifiers).
- Sailors amounting to thelocal sailors reserves divided by 4.
After a province has been raided, its loot bar is emptied, the amount ofdevastation is increased by10%, and the“Raided Coast”modifier is applied for ten years. Each raided province will add a−25opinion penalty with the raided country (up to a maximum of−100), decaying by+1per year.

Raiding efficiency is reduced by the number of guns foreign fleets onpirate hunting patrolhave, compared to the raiding fleet.

If the raider has access to the piratefactions, using the "Raid coast" interaction gives1Buccaneers influence.

##### "May raid coasts" ability[edit|edit source]

A country can raid coasts if it has the abilities“May raid coasts”or“May raid coasts including coasts of countries with same religion”. They can be gained by the following:

- Knights Hospitaller tradition (The Knights)
- Siddi tradition (Habsan)
- Has enacted theT1 government reformBarbary Iqta(for Muslim countries with Maghrebi culture)
- Has enacted theT1 government reformBarbary Eyalet Government(foreyaletswith Maghrebi culture)
- Has enacted the T4 government reformEmbedded Norse Traditions(forNorsecountries)
- With the"Maghrebi Corsairs" naval doctrine (with Maghrebi culture)
- Has completed amission which temporarily gives the ability to raid coasts (Aragon,France)
- Norse tradition (Norse nations)
- Somalian tradition (Somalia)
- Norman ambition (Normandy)
- Has enacted theT1 government reformPirate Republic
#### Blockading[edit|edit source]

Fleets will automatically blockade a coastal sea province under hostile control while they are stationary and have no other orders.

##### Blockade power[edit|edit source]

The blockade power (sail speedin the tooltip) of a fleet is displayed after theblockade icon in the fleet panel. It is mainly determined by thetactical movement speed of the fleet's ships.

Each point of blockade power will be able to blockade one development point of a province.

Blockades will only take effect if there is enough blockade power to match the full development. If a fleet does not have enough blockade power to blockade all adjacent provinces under hostile control, it will assign its blockade power in precedence of:

- Hostile province under a siege lead by any friendly force
- Hostile province with the lowest development
- Hostile rebel province with the lowest development
Thedetach blockadebutton () in thefleetpanel will detach a fleet of sufficient size to blockade all enemy ports neighboring the sea province.

Blockade efficiency is determined by:

Ideas and policies:

- Maritime idea 7: Naval Fighting Instruction
- Naval-Maritime: The Naval Supremacy Act
- British idea 7: Britannia Rules the Waves
- Omani ambition
Decisions and events:

In order to properly blockade a province with your fleet (i.e. inflict the effects of a blockade on the province), the blockade power has to be at least the development of the province. The "Coastal Defence" and "Naval Battery" increase the required blockade power according to their modifers. For example, if your coastal province has20development and you have a Naval Battery in the province, the enemy fleet will need to have a blockade power of40in order to give the full blockade effects to the province. In essence, the 'Blockade Force Required' modifier increases the threshold for blockade power to fully blockade the province.

Blockade force required is determined by:

##### Effects of blockade[edit|edit source]

A blockade has a number of effects on any neighbouring land provinces occupied by an enemy:

Notably, provinces producingSpices get negative monthly devastation that exactly counteracts the positive modifier from blockades.

Blockading a country's ports also applies the following modifier, scaled by proportion of (core, state) development blockaded:

Being 100% blockaded also gives the following Debuffs :

- −75%Global Trade Power
- −75%Trade Steering
Blockades have the following further effects:

- Siege:−2penalty to die rolls in non-blockaded coastal provinces, except those owned by primitives. (Provinces without ports, e.g. on the Caspian Sea, don't count.)
- War score: Blockades are worth war score scaling with the proportion of development they represent and local autonomy. Capital and fortified provinces are worth more. Somecasus bellihave blockades as a war goal.
- Spoils of War: Blockades addducats to the blockader's treasury (listed under "Spoils of War") in proportion to the province's income.
- Restriction of movement: See§ Blocking a straitbelow.
#### Blocking a strait[edit|edit source]

To block a strait the following requirements must be met:

- The blockading alliance or a neutral nation have to control (owns or occupied) at least one side of the adjacent provinces
- The blockading alliance have to control the sea by a naval force (blockade efficiency doesn't matter)
As a consequence, if a war alliance controls both sides of the strait they can march over regardless of blockades.

Examples:

- A war participant controlling both sides of a strait: The Ottomans can cross the strait at Bosphorus as long as they have control of Constantinople and Kocaeli even when the enemy controls the sea. Same system applies for the second strait between Gelibolu and Biga.
- A neutral nation controlling a side of a strait: Ulster, controlling Ulaidh, cannot cross the strait across the Irish Sea to Ayrshire in Scotland if Ulster is only at war with England (Scotland is neutral and gives military access to one of the war participants), and England controls the Irish Sea.
- However, if Ulster has called in an ally, say Burgundy, and Burgundy is in a separate war with Scotland and controls Ayrshire, then the first requirement is no longer fulfilled, and the Irish nation can cross the strait despite England having control of the Irish Sea.
Besieging a province of a strait does not fulfil the first requirement; the siege must finish, translating to control.

### Naval missions[edit|edit source]

Fleet missions are grouped together under a collective “Select Mission” button () that allows the player to tell their fleets to;

- Protect Trade
- Privateer
- Hunt Pirates
- Explore
- Hunt Enemy Fleets
- Blockade Enemy Ports
- Intercept enemy fleets
#### Protect trade[edit|edit source]

This mission is available to any fleet that contains light ships. It will add the trade power of the light ships in the fleet to any maritime trade node that the player already has some trade power in, provided that the trade node is within both trade range and supply range.

The trade power of light ships depends on ship model, and increases as diplomatic technology advances. Furthermore, it scales linearly with the naval maintenance slider, reaching full potential at maximum naval maintenance, but suffering a−75%penalty at minimum naval maintenance. AI nations do not suffer a trade power penalty to light ships from low naval maintenance.

#### Privateer[edit|edit source]

This mission is available to any fleet that contains light ships. The fleet will hoist the Jolly Roger and add the trade power of its light ships to a pirate nation in any selected trade node. Unlike the protect trade mission, existing trade power is not needed in a trade node to start a privateer mission.

##### Privateer efficiency[edit|edit source]

Light ships on privateer missions receive a+50%bonus to their trade power. Privateers do not inherit any national bonuses or penalties to global trade power. Factors such asoverextension or halved trade power when collecting in foreign nodes are notably ignored. The trade power of privateers is instead affected by various privateer efficiency modifiers:

- Mercenary-Exploration: Transportation Act
- Offensive-Exploration: Sponsored Privateers
- Palembang idea 3: Controlling the Strait
- Espionage idea 6: Privateers
- Maritime idea 7: Naval Fighting Instruction
- Cebu idea 5: 'The Place for Trading'
- Mindanao idea 7: Pirates of Mindanao
- Naxian idea 3: Archipelago Of Opportunities
- Barbary Corsair traditions
- Cornish idea 4: Pirates of Penzance
- Dithmarscher idea 4: Expert Wreckers
- Kono idea 7: Murakami Suigun
- So idea 4: Bahan Ship
- East Frisian traditions
- Gutnish traditions
- Al-Haasa idea 7: Legacy of Rahmah ibn Jabir
- Arakanese idea 4: Magh and Ferenghi
- Betsimisaraka idea 2: Pirate Ports
- Cypriot idea 7: Raid Turkish Commerce
- Malagasy idea 3: Pirate Ports
- Montenegrin idea 4: Balkan Gusars
- Moroccan idea 5: Protect Pirate Republics
- Munster idea 6: Pirate Haven
- Norman idea 5: Viking Raids
- Novgorod idea 6: Funding the Ushkuiniks
- Pattani idea 4: Lian Dao-Qian Band
- Pomeranian idea 1: Legacy of Pirates
- Sumatran idea 3: Spice Pirates
- Berber idea 4: Corsairs
- Sonoran idea 5: Taking What’s Ours
- Tunisian idea 3: Corsairs
The trade power of ships assigned to the privateer mission affect the trade power they have in the node, this means that the Trade Route Mapflagship modification(giving +1 trade power per ship in fleet), the Merchant Navynaval doctrine(giving +33% ship trade power), as well as other ship trade power modifiers, affect privateers.

TheEnlist Privateersdecision increasesprivateer efficiency by another+25%. It becomes available at8Diplomatic technology and requires the nation to have completedMaritimeideas, a ruler with3Military, as well as50%of theforce limit.

Winning aparliament debate "Issue Letters of Marque" provides+15%privater efficiency for 10 years.

Each point of naval tradition also increases privateer efficiency by0.25%. The total trade power from privateers is thus

Notethat withoutWealth of Nations,El Dorado,Mare Nostrum ,Golden CenturyorLions of the North DLC enabled the modifiers are exchanged. Privateer efficiency is replaced by trade power abroad.

##### Range[edit|edit source]

Privateer fleets can only reach trade nodes in sea zones that are withintrade range. A nation's trade range extends from cored provinces of the nation or its junior partners, colonial nations and client states.

Trade range can be increased by diplomatic technology, decisions, ideas, and policies:

- Ryukyuan idea 4: Maritime Commercialism
- Swahili traditions
- Maritime idea 1: Merchant Traditions
- Trade idea 3: Merchant Adventures
- Kilwan idea 1: Kilwan Latitude Staves
- Trading City idea 6: City of Great Reach
- Gujarat Sultanate idea 2: Jain Connections
- Gujarati Princedom idea 7: Extend Trade Routes to Africa
- Horn of African idea 2: The Land of Punt Legend
- Kono idea 6: Trade With Continental Asia
- Malabari idea 1: Merchants of Southern India
- Mesoamerican idea 7: Obsidian and Jade
- Mogadishan idea 1: Indian Ocean Trade
- South Indian idea 1: Merchants of Southern India
- Lübeckian traditions
- Sumatran traditions
- Evenk idea 2: Reindeer Herding
- Indigenous-Trade: Commercial Tribes
- Dutch idea 2: Dutch Trading Spirit
- East India idea 5: Intercontinental Trade
- Mamluk (upgraded) idea 1: Red Sea Trade
- Mamluk idea 1: Red Sea Trade
- United Crowns idea 4: Dutch Trading Spirit
- West Indies idea 4: The American Trade Hub
##### Effects[edit|edit source]

The privateer fleet increases the trade power of a pirate nation that acts as a collector in the trade node. This pirate nation will submit50%of its earnings to the nations that commissioned the privateers contributing to its trade power. The presence of this pirate nation effectively reduces the share of trade value controlled by all non-pirate nations in the node. Income from privateering will be recorded in the economy window asspoils of war.

Any country that would have more than20%of the trade power in the node without privateers will receive a casus belli against any nation that has sent privateers to that node.

Any country that would have more than10%of the trade power in the node without privateers will have a−1opinion modifier per month of any nation that has sent privateers to that node, capped at−100.

Sending light ships on privateer missions against rivals grants up to 10power projectionmonthly per country.

Activating a privateer mission will force the game to update a nation's power projection on the next game day. This will consequently update, among other things, the trade power in trade nodes and the nation's military force limits. Triggering an update like this can be useful when game stats are temporarily desynchronized due to certain actions, such as sending light ships to protect trade or changing local autonomy levels.)

Privateers also capture a portion of the ducats carried intreasure fleetspassing through the node in which they operate.

#### Hunt pirates[edit|edit source]

This mission is available to fleets which contain at least one ship that isn't a transport. Fleets containingheavy ships orlight ships may hunt pirates in anytrade nodewhich is notinland; however, fleets containing onlygalleys (as well as fleets which are a mixture of galleys and transports) can only hunt pirates in nodes where all nearby sea provinces areinland seas, e.g. in Basra and Alexandria, but not in Hormuz. This does not necessarily mean that fleets will only hunt in inland sea provinces (where they are more effective): for instance, a fleet hunting pirates in Canton will use the Luzon Strait.

The totalnumber of guns of the ships is used to find the efficiency at which they hunt the pirates. Thetrade power of pirates is reduced by hunt pirate efficiency. This means that it reducesprivateering efficiency from 0%, when no fleet is hunting pirates, up to 99%, if the total number of guns from the hunting fleet is greater than or equal twice the total number of guns from pirating fleet. It is important to note that the reduction of privateering efficiency will not stop privateering fleets from stealing trade income if that fleet has any bonuses to its privateering efficiency.

In addition, it is helpful to know that this is also effective at stopping other nations from raiding your coasts.

Note that pirate fleets and fleets hunting pirates do not actually battle or otherwise damage each other, unless the countries that own the fleets are at war with one another.

#### Explore[edit|edit source]

This mission requires an explorer, and a total of 3 light and/or heavy ships. It sends the fleet to explore a region or a coast line, that can be chosen by either selection the region on the UI or clicking on the naval TI with the "explore" tab opened, and the player can attempt to circumnavigate the globe atdiplomatic technology9.

#### Hunt enemy fleet[edit|edit source]

The fleet will hunt enemy fleets in a specific sea region, that can be chosen by either selecting the region in the UI or clicking on the naval region with the tab opened.

#### Blockade enemy ports[edit|edit source]

The fleet will blockade enemy ports and evade enemy fleets that are not significantly weaker. (Can be altered by setting the fleet to be Bold.)

#### Intercept enemy fleets[edit|edit source]

This mission will have the fleet seek out enemy fleets near allied coastlines, focusing on troop transports.

### Strategies and tactics[edit|edit source]

#### Deployment[edit|edit source]

Decisive wins can be achieved in battle by concentrating all battle ships (heavies and galleys) in one fleet up to just a little over the engagement width, with a re-enforcement fleet in the neighbouring tile. Seek battle if one has superior naval assets, and avoid engagement otherwise.

When ready to attack detach and send only the front line (your best ships and flagship up to the value of your engagement width and a few more) into battle. Then as the phases progress feed reinforcements every few days from your neighbouring reinforcing fleet piece-meal into the battle to replace destroyed or disengaged ships. This will reduce morale losses from having as few ships as possible in the reserve line in the battle. One could call it the "just-in-time" re-enforcement method.

Remember to maximise your engagement width by using your highest manoeuvre admiral, preferably with high shock and fire pips too. You want more ships than the enemy to all be firing at the same time.

Naval admirals can significantly tilt a battle in one's favor, even more so than generals; without an admiral, stack wiping and sometimes even victory becomes unlikely even with a seemingly overwhelming advantage.

However, other factors may complicate this. A country may be forced to divide their fleet if they have naval objectives other than destruction or suppression of the enemy navy, such as protecting (multiple) trade nodes, transporting land units by sea, exploring, patrolling for pirates, reconnaissance, blockading and so forth. If the country lacks naval supremacy compared to their enemies, they may be forced to risk losses, support fewer of these objectives at the same time, or leave the sea entirely for the duration of the war.

However, even if you are weaker than the enemy, tactics may make the difference in a long drawn out war. Smartly engage one enemy stack at a time (using the techniques above) whenever the odds are materially in your favour to win that specific battle. A sequence of such victories can quickly add up to war score and help ensure the enemy cannot land their troops.

Be sure to sail your full stacks into ports where you have coastal forts with terrain penalties for the besiegers. The enemy will be lured into sieging these unfriendly forts if they don't see your stacks nearby, while having fleets allow you to sail into these coastal forts before they can withdraw. Such attacks can lead to quick stack wipes of the enemy and can dramatically turn the war in your favour.

#### Bringing an enemy fleet to battle[edit|edit source]

A country with a naval advantage may wish to bring a reluctant enemy fleet to battle. This can be accomplished in several ways:

- If the enemy fleet is docked at a port, they cannot be attacked directly. However, the fleet may be ejected by occupying (successfully sieging) that province, at which point the leaving fleet will enter into combat with any opposing fleet(s) in the corresponding sea province.
- A small "bait" fleet may be used to lure the enemy into attacking, whereupon the main fleet can reinforce from a nearby sea province or port. This can also be used to lure fleets into or out of inland seas, where galleys have a relative advantage.
- Light ships move faster than heavy ships / transports, which move faster than galleys. A fleet without galleys can easily catch an enemy fleet that contains galleys.
- Putting your ships into port will usually cause the AI navy to be more aggressive and leave port, sometimes even attempting a full blockade, leaving their navy significantly more vulnerable.
- After a defeat, an enemy navy will typically retreat to an adjacent port. Having an army already sieging down this port will give you a significant advantage, as the ships will be forced to leave port soon after arriving while having low morale and no repairs, allowing for a stackwipe or a victory in which they may lose most of their ships.
- Sometimes a bug will allow the AI to remain permanently in a province even if it is sieged down. The only way to fix this is to retreat several sea tiles from the province and then go into port, or in other words give the ai an illusion of safety.
### Footnotes[edit|edit source]

1. ↑See in/Europa Universalis IV/common/defines.lua:HEAVY_SHIP_COMBAT_WIDTH, LIGHT_SHIP_COMBAT_WIDTH, GALLEY_COMBAT_WIDTH and TRANSPORT_COMBAT_WIDTH.
1. ↑See in/Europa Universalis IV/common/defines.lua:NAVAL_BASE_ENGAGEMENT_WIDTH.
1. ↑See in/Europa Universalis IV/common/defines.lua:GALLEY_BONUS_INLAND_SEA
1. ↑See in/Europa Universalis IV/common/defines.lua:GALLEY_BONUS_COASTAL_SEA