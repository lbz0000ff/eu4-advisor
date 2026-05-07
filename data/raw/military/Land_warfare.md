Please help with verifying or updating older sections of this article.At least some were last verified forversion1.24.

Land warfare is the deployment and maneuvering of military assets against an enemy, in most cases this results in combat between opposing armies. In EUIV most combat is land-based and, while thenavalaspect of war holds importance, losing the land war is usually the main cause of defeat. The art of land warfare is therefore of significant importance, and its complexities are discussed here as fully as possible.

### Contents

- 1Combat interface
- 2Terrain2.1Crossing penalties2.2Battles in a province under siege2.3Simultaneous arrival
- 2.1Crossing penalties
- 2.2Battles in a province under siege
- 2.3Simultaneous arrival
- 3Deployment3.1Army composition3.2Combat width3.3Initial unit deployment3.3.1For the smaller army3.3.2For the bigger army
- 3.1Army composition
- 3.2Combat width
- 3.3Initial unit deployment3.3.1For the smaller army3.3.2For the bigger army
- 3.3.1For the smaller army
- 3.3.2For the bigger army
- 4Combat sequence4.1Overrun4.2Phases4.3Target selection4.4Base casualties4.5Casualties multiplier4.6Morale casualties (i.e. Morale damage)4.6.1Morale casualties taken by the backline4.6.2Morale casualties taken by the reserves4.7Strength casualties4.8Retreat and reinforcements4.9Overkill
- 4.1Overrun
- 4.2Phases
- 4.3Target selection
- 4.4Base casualties
- 4.5Casualties multiplier
- 4.6Morale casualties (i.e. Morale damage)4.6.1Morale casualties taken by the backline4.6.2Morale casualties taken by the reserves
- 4.6.1Morale casualties taken by the backline
- 4.6.2Morale casualties taken by the reserves
- 4.7Strength casualties
- 4.8Retreat and reinforcements
- 4.9Overkill
- 5Combat statistics5.1Military tactics5.2Pips5.3Flanking range5.4Morale5.4.1Modifiers5.4.2Morale recovery5.5Cavalry to infantry ratio
- 5.1Military tactics
- 5.2Pips
- 5.3Flanking range
- 5.4Morale5.4.1Modifiers5.4.2Morale recovery
- 5.4.1Modifiers
- 5.4.2Morale recovery
- 5.5Cavalry to infantry ratio
- 6Forts6.1Fort level and garrison6.2Fort maintenance6.3Zone of control6.4Sieges6.4.1Sortie6.4.2Siege ability6.4.3Fort defense6.4.4Phases6.4.5Dice roll6.4.5.1Siege bonuses6.4.6Effects6.4.7Artillery barrage6.4.8Naval barrage6.4.9Assault
- 6.1Fort level and garrison
- 6.2Fort maintenance
- 6.3Zone of control
- 6.4Sieges6.4.1Sortie6.4.2Siege ability6.4.3Fort defense6.4.4Phases6.4.5Dice roll6.4.5.1Siege bonuses6.4.6Effects6.4.7Artillery barrage6.4.8Naval barrage6.4.9Assault
- 6.4.1Sortie
- 6.4.2Siege ability
- 6.4.3Fort defense
- 6.4.4Phases
- 6.4.5Dice roll6.4.5.1Siege bonuses
- 6.4.5.1Siege bonuses
- 6.4.6Effects
- 6.4.7Artillery barrage
- 6.4.8Naval barrage
- 6.4.9Assault
- 7Mechanics of an army7.1Exile7.2Looting7.3Attach to army7.4Attack natives7.5Scorched earth7.6Rebel suppression7.7Forced march
- 7.1Exile
- 7.2Looting
- 7.3Attach to army
- 7.4Attack natives
- 7.5Scorched earth
- 7.6Rebel suppression
- 7.7Forced march
- 8References
### Combat interface[edit|edit source]

Combat is not only determined by mere numbers such as modifiers and dice-rolls, but through a complex simulation in which units deployed into two rows of positions for each side, allowing units to fight the enemy units in front of them, the enemies at their flanks if possible (with high enough flanking range), and move between different positions if needed. All the while, the system retreats destroyed or low-morale units and deploys reinforcements and reserves as well.

The combat system, while not being entirely obvious or intuitive, can be seen through the combat interface which allows the player to see which regiment is fighting which, and which is moving where.

### Terrain[edit|edit source]

Terrain for each province is shown in both theterrainandsimple terrainmapmodes.Terrainshows a natural-looking map, whilesimple terraincolor-codes each province by its terrain type; both have tooltips showing terrain type, fort level, and the current winter, if any. Some terrain imposes a movement speed penalty to armies traveling in the province in addition to a negative rough terrain modifier to the attacking army, with different types of terrain having different modifiers.

Here is a list of the types of terrain and the modifiers which they grant.

#### Crossing penalties[edit|edit source]

A crossing penalty that reduces all dice rolls is applied to the attacker under the following circumstances:

- Crossing a river:−1to all rolls.The presence of a river in between a province and its neighbors is indicated in the province window, through a small river icon. Mousing over this icon will show which neighboring provinces require a river to be crossed in order for an army to reach the province.
The presence of a river in between a province and its neighbors is indicated in the province window, through a small river icon. Mousing over this icon will show which neighboring provinces require a river to be crossed in order for an army to reach the province.

- Crossing a strait:−2to all rolls. Seestraitsfor a list.
- Amphibious landing:−2to all rolls. This includes an attack from sea or a landing directly with ships at port.
For attackers that originate from multiple provinces, they will all receive the crossing penalty if any one of them would normally receive it alone. All crossing penalties are removed if the attacking leader has a higher maneuver rating than the defending leader. The check on leader maneuver rating is performed daily, so a high maneuver leader can still swing the tide of battle even if he joins an engagement late.

#### Battles in a province under siege[edit|edit source]

Normally, the "attacker" is defined as whichever side moves into a given province last, while the "defender" is whichever one was already occupying the area. However, if a given army is in a province which contains a hostile fort, the roles are switched: the army which was in the province first is treated as the "attackers", and those which arrive afterwards are the "defenders" as they are attempting to break the siege. Attacker penalties from terrain are applied to the "siege" army, while attacker penalties from river/strait crossings are nullified regardless of any leaders' maneuver pips. This even applies if the army is not actually sieging or if the fort is hostile to both armies.

The player can take this into account when building forts, as well as when choosing which provinces to siege and which besieged provinces to prioritize sending their troops to.

If a sieging army wins a battle on a province where they're sieging, an immediate bonus siege tick is triggered. This does not reset the ticking down for the next siege tick.

#### Simultaneous arrival[edit|edit source]

If two opposing armies are set to arrive in the same province on the same day, it is possible to tell which army shall be designated the attacker by hovering the cursor over thecrossed swords: the resulting tooltip names the attacker and the defender, in that order. This order is based on the tag order (seeCountries).

### Deployment[edit|edit source]

#### Army composition[edit|edit source]

To maximize the effectiveness of an army, a proper mixture of troops is important.

#### Combat width[edit|edit source]

Combat width determines how many units can actively participate in a battle at one time. For every 1 combat width, 1 additional regiment can be placed in the front and back rows, if sufficient troops are available.

All units that are not placed on the battlefield either in the front or the back row are said to be inreserve. They don't take part in the actual combat, although they still suffer from passive moral damage (see below), and they can rejoin the ongoing battle if space becomes available in either the front or the back row.

The base combat width is 15.[1]As military technology advances, a country's combat width increases, allowing them to use more soldiers effectively at once. All countries other than Native Americans start with tech level 2 or 3, so their starting combat width will be 20. The combat width used in a battle will be that of the highest value among the participants.
Here is a table of combat width by military technology level.

#### Initial unit deployment[edit|edit source]

The game uses an undocumented algorithm to automatically deployland unitson the battlefield for each side of the battle. Through observation and controlled experiments, the community has suggested a theory that the game seems to follow, dependent on the rough size andcompositionof eacharmy.

##### For the smaller army[edit|edit source]

- If there is not enough infantry to fill the entire first row, the game will prioritize to:Deploy all infantry in the first row.Deploy as much cavalry as possible to the sides of the first row.Deploy all artillery in the second row. If there are more units in the second row than the first, then it will redeploy artillery to the first row until both rows are even.
1. Deploy all infantry in the first row.
1. Deploy as much cavalry as possible to the sides of the first row.
1. Deploy all artillery in the second row. If there are more units in the second row than the first, then it will redeploy artillery to the first row until both rows are even.
- If there is enough infantry to fill the entire first row, the game will prioritize to:Deploy all infantry in first row, except for X[Unknown value]positions to each side.Deploy X units of cavalry on each side of the first row.Deploy all artillery on the second row.
1. Deploy all infantry in first row, except for X[Unknown value]positions to each side.
1. Deploy X units of cavalry on each side of the first row.
1. Deploy all artillery on the second row.
##### For the bigger army[edit|edit source]

For an army bigger than the combat width, the game will prioritize to:

1. Deploy all infantry in the first row that can be positioned to attack enemy units in the first row, except for X[Unknown value]positions to each side.
1. Deploy all cavalry in the first row that can be positioned to attack the enemy units in the first row.
1. Deploy all artillery in the second row.
The deployment of allied regiments within a multinational army is similarly undocumented. It can be observed that units belonging to the combat leader (e.g. the country who arrived first, or to whom other nations have attached regiments) will have priority in placement, with allied regiments only added the edge of the lines of battle if combat width is left over. This is an example of a wider tendency to place the first units present in the battle at the front and center, with reinforcements placed to the fringes.

### Combat sequence[edit|edit source]

When two hostile armies meet in a province a battle will commence. A battle will last until one side is routed or annihilated.

#### Overrun[edit|edit source]

Combat will not happen if one side outnumbers the other by a factor of10or more. Instead, the armies of the smaller side are instantly destroyed. This is referred to as anoverrunor, colloquially, aninsta-wipeorinstant stackwipe. Unlike a normal stackwipe, morale is not a factor. A side which is big enough to fill the combat width of the battle can't be overrun (even if they do not actually fill the combat width, because some of the regiments are artillery). A side also can't be overrun if it is least2 institutions ahead of the other side.

#### Phases[edit|edit source]

Combat is divided into a series of 3-day phases. Phases alternate between Fire and Shock, with the Fire phase happening first.

At the beginning of each phase, each side rolls a dice. The result is used to determine the morale damage and casualties inflicted to the opponents each day in the three-day-phase.

Generally, during the shock phase, cavalry is the most powerful and during the fire phase, infantry. Artillery gradually becomes the most powerful unit during the fire phase as it gains powerful modifiers to fire with technology, such as a+1modifier at military technology 16 and up to a total of+8.4(cumulative) at military technology 32.

Some bonuses exist to directly increase the dice roll result:

#### Target selection[edit|edit source]

Units in the front row can attack any enemy unit within their horizontal flanking range. Generally they will only engage enemies that are directly ahead of themselves, but they can sometimes execute flanking attack if more effective atreducing the enemy's combat ability. This typically occurs if the unit is facing an enemy artillery regiment or a particularly outdated unit; in this case the unit may choose to attack the flanks of a stronger enemy unit nearby. Artillery are the only units that can attack from the back row but they will only deal 50% damage from that position (this percentage can be increased by certain modifiers, as detailed atLand units#Damage from Backrow).

#### Base casualties[edit|edit source]

The base casualties describe the impact of leaders, unit types, random dice roll, as well as terrain on the battle. Note that the result of this formula cannot go below 15.

- Dice roll (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DiceRoll}}): A random number between 0–9, rolled for each side at the beginning of each phase (not each day).
- Dice Roll Bonus (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DiceRollBonus}})
- Leader fire / shock skill (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{Leader}}).
- Enemy leader fire / shock skill (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{EnemyLeader}}).Note that the leader skill bracket cannot be negative, meaning that the side with the better general will get a bonus to its base casualties, equal to the difference in pips between its leader and the opposing side's leader, but the other side with the worse general will not receive any penalty.
- Note that the leader skill bracket cannot be negative, meaning that the side with the better general will get a bonus to its base casualties, equal to the difference in pips between its leader and the opposing side's leader, but the other side with the worse general will not receive any penalty.
- Unit offensive pips (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{OffensivePips}}): Offensive morale pips + offensive fire/shock pips (each in its relevant phase)[2]for morale casualties and offensive fire / shock pips only for strength casualties.
- Targeted regiment's defensive pips (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DefensivePips}}): Defensive morale pips + defensive fire/shock pips (each in its relevant phase)[2]for morale casualties and defensive fire / shock pips only for strength casualties.
- Terrain modifiers (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{Terrain}}): Harsh terrain may give a penalty to the attacks of the attacking army.
#### Casualties multiplier[edit|edit source]

Multipliers affecting both morale and strength casualties:

- Regiment's strength (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{Strength}}): Number of soldiers left in the regiment.
- Regiment's fire / shock base damage technology modifier (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{TechModifier}}): Determined by current military technology level for a particular type of units (infantry/cavalry/artillery) SeeCumulative mil tech effects to army. Can be increased with some ideas, like Spain's +1 Artillery fire.
- Target unitMilitary Tactics (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{MilitaryTactics}}). Note the importance of relative tactics differences; as the denominator it impacts all factors and hence 0.25 for the enemy leads to a 4 multiplier (1/0.25) while a higher tactics number of say 0.5 leads only to a 2 multiplier (1/0.5)
- Regiment's Combat Ability (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{CombatAbility}}).
- Regiment's Discipline (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{Discipline}}): Discipline also increases Military Tactics, so it indirectly increases regiments' defense. Discipline for special units and mercenaries also impacts both the offensive and defensive capabilities of the unit.
- Battle length (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{BattleLength}}): The casualties are increased by 1% per day of the battle, starting at +1% on the first tick.
#### Morale casualties (i.e. Morale damage)[edit|edit source]

- Base casualties(Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{BaseCasualties}}).
- Shared multipliers(Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{Multipliers}}).
- Regiment's morale dealt damage modifier (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DamageModifier}}).
- Target regiment's morale damage received (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DamageReceived}}).
- Regiment's max morale (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{MaxMorale}}).
- All regiments present in a battle (both front and backrow) take base morale damage (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{PassiveMoraleDamage}}) equivalent to 1% of the average max morale of all regiments on the opposing side.
On top of the damage taken by the frontline, the backline (ie. the cannons)will take 40% of the frontline's morale casualties.This effectively means that in a battle that started with full backline and frontline, where the frontline is constantly refreshed, the backline will end up retreating roughly after the 3rd frontline reaches slightly less than 50% of its morale.

All regiments present in a battle, but which aren't engaged in it at given moment, ie. the reserves, will take base morale damage similar toFailed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{PassiveMoraleDamage}}equivalent to 2% of the average max morale of all regiments on the opposing side.

These casualties, in contrast to the base morale damage taken by frontline, can be reduced by the "Reduced morale damage taken by reserves" modifier, such as the -50% reduction from having 80% professionalism or more.

Ideas and conditions that increase morale damage dealt:

- Navarran traditions
- Ulster idea 1: Highland Connections
- Court-Offensive: Sharp Wits Act
- Revolutionary French idea 2: Elan!
- Quality-Religious: The Military Zeal Act
- forCaroleansregiments (available only toSweden)
#### Strength casualties[edit|edit source]

- Base casualties(Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{BaseCasualties}}).
- Shared multipliers(Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{Multipliers}}).
- Regiment's fire / shock damage modifier (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DamageModifier}}).
- Targeted regiment's fire / shock damage received (Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{DamageReceived}}).
There are several unique national ideas which modify the amount of damage inflicted and received in both the fire and shock phases.

Ideas and conditions that increase fire damage dealt:

- Alaskan idea 4: Bear Hunting
- Most Serene idea 4: A Gunpowder Republic
- Anglo-Dutch traditions
- Cirebonese idea 4: Mount Ciremai
- Date idea 4: Dragon Corps
- Dutch idea 7: Platoon Fire
- Egyptian idea 5: Westernize the Military
- English idea 5: Redcoats
- Evenk idea 7: New Ways to Hunt
- Hatakeyama idea 7: Saika-shu
- Hindustani idea 5: Gunpowder Empire
- Ilkhanid idea 7: Recruit Turkoman Gunners
- Isshiki idea 5: Inadome Gunnery
- Jaunpuri idea 1: Purbias
- Korean idea 3: Choi Mu-Seon Gunpowder Engines
- Mewari idea 6: Mandatory Firearm Drills
- Mysorean idea 5: Rockets!
- Münster idea 6: Bommen Berend
- Oda idea 5: Triple Firing
- Palawa idea 6: Survivors of the Black War
- Plains Native idea 2: Bow Archery
- Rajputana idea 4: Purbia Legacy
- Shimazu idea 5: Tanegashima
- Smolenskian idea 2: The Armories of Smolensk
- Sonoran idea 4: Cowboy Country
- Texan idea 2: Texan Revolution
- Tirhuti idea 4: Purbias
- Utsunomiya idea 2: Legacy of Nasu no Yoichi
- Beninese ambition
- Bregenzer ambition
- Dhundhari ambition
- Nubian ambition
- Saxe-Lauenburg ambition
- Hanoverian idea 3: Schützenfest
- forStreltsyregiments (available only to East Slavic countries)
- with ageneralwho has the ‘Ruthless’leader trait
- withThe Guns of Songhaimodifier from missions ofSonghai
- withUpdating the Militarymodifier from missions ofItaly
- withProfessional Themata Soldiersmodifier from missions ofByzantium
- withThe Sisterhood of Jeanne d'ArcTier 1 reform (available only toOrleans)
- forZoroastrian countries with theBaku Ateshgahmonument onmagnificent level
- depending onarmy professionalism
- depending on regimentdrill
Ideas and conditions that increase shock damage dealt:

- Norse idea 5: Berserkir
- Palawa idea 3: Darwin Glass
- Highlander idea 5: Highland Charge
- Kamilaroi traditions
- Muscovite traditions
- Australian idea 6: Integration of the Bushrangers
- Corsican idea 1: The Unblinded Moor
- Danish idea 4: Royal Mercenaries
- Great Yuan idea 4: Keshik and Weijun
- Kiwi idea 4: The Kiwi Haka
- Larrakia idea 5: Ceremonial Scarring
- Nagpuri idea 5: Light Cavalry Shock Tactics
- Nanbu idea 6: Chosonji Temple
- Timurid idea 3: Unleash the Tiger
- Trent idea 6: Mountain Warfare
- Zulu idea 3: The Impi Warriors
- Aboriginal ambition
- Cossack ambition
- Horde-Diplomatic: Fear Tactics
- Horde-Expansion: War Horses
- Influence-Quantity: Guerrilla Warfare
- forCossackregiments (available only to countries with theCossacks estate)
- for following or inviting a scholar from theShiaJafarischool
- depending onarmy professionalism
- depending on regimentdrill
Ideas and conditions that reduce fire damage taken:

- Andalusian idea 1: Stand Against the Reconquista
- Hanoverian idea 7: King’s Legion
- Texan traditions
- Divine idea 2: By the Grace of God
- Leinster idea 4: He Who Is Not Strong Must Be Cunning
- Russian idea 7: Broaden the curriculum of the Cadet Corps
- Latgalian ambition
- Horde-Innovative: The Best Defense
- forJanissaryregiments (only recruitable withOttoman government types)
- forZoroastrian countries with theBaku Ateshgahmonument onsignificant level
Ideas and conditions that reduce shock damage taken:

- Tiwi traditions
- Ando idea 1: March of Akita
- Rassid idea 5: Mountain Strongholds
- Dithmarscher traditions
- Hisn Kayfan (Ayyubid) traditions
- Hisn Kayfan traditions
- Manipur traditions
- Orissan traditions
- Sistani traditions
- Yi traditions
- Assamese idea 3: River Warfare
- Baluch idea 2: Hani and Sheh Mureed
- Hausan idea 5: Sarkin Yaki
- Irish idea 1: Irish Endurance
- Kanem Bornuan idea 5: Fixed Military Camps
- Lur idea 1: Kingdom in the Zagros Mountains
- Butua ambition
- Bohemian (upgraded) idea 3: Wagenburg
- Bohemian idea 3: Wagenburg
- Horde-Innovative: The Best Defense
- forJanissaryregiments (only recruitable withOttoman government types)
- with ageneralwho has the ‘Defensive Planner’leader trait
- for following or inviting a scholar from theShiaZaidischool
#### Retreat and reinforcements[edit|edit source]

Units deployed on the battlefield (either in the front or the back row) retreat when they individually reach either 0 morale or 0 regiment strength, thus freeing the space they previously occupied on the battlefield.Retreatedunits do not take part in the battle anymore and are accounted for separately in the combat interface.

When free space is available on the battlefield, either because defeated units retreated or because the combat width wasn't filled up to begin with, units held in reserve (including any new army that arrives in the province to join the ongoing battle) can begin to be deployed into the combat: these arereinforcements.

Reinforcements obey the following rules:

- Infantry/cavalry will always instantly deploy to fill any available space in the front row up to the combat width; it will never deploy to the back row and any remaining unit once the front row is entirely filled will stay/go to the reserve.
- Artillery will instantly deploy to the front row up to theenemycurrent (not maximal) combat width.
- If both infantry/cavalry and artillery are available to fill the front row, in principle, infantry/cavalry will take precedence (further testing needed).
- Once the front row is filled in accordance with the rules above, any artillery remaining in the reserve will be deployed to the back row at a rate of 2 regiments per day + 1 regiment per 2 maneuver pips of the commanding general (rounded down).[3]A tooltip in the combat interface displays this value.
In older versions of the game (before patch 1.34) a bug existed where regiments that reached 0 strength before morale reached 0 during the first 12 days of a battle would not retreat like they normally would. Instead, when this occurred, the 0-strength regiment stayed on the front line until the first 12 days passed. This remained true even when the 0 strength regiment reached 0 morale during the first 12 days. This behaviour was known as "zombie regiments". Devs claimed to have removed the zombie regiment bug as of version 1.34.[4]

#### Overkill[edit|edit source]

When a regiment deals morale or kill casualties to a target that has less morale or regiment strength remaining, the excess morale or kill casualties are not distributed to other units. Thus a regiment that has 0.01 morale left after a phase will absorb an entire other day of kill & morale casualties.

### Combat statistics[edit|edit source]

#### Military tactics[edit|edit source]

Military tactics reduces the amount of damage a country's troops take in combat. Military tactics is increased bymilitary technology. It is also multiplied by discipline.

Some ideas may increase military tactics:

- Revolutionary French idea 6: Napoleonic Tactics
#### Pips[edit|edit source]

Each military unit has offensive and defensive stats in three categories: fire, shock, and morale. Offensive stats are represented by yellow pips, and defensive stats by green pips. During each combat phase, each unit will use its offensive pips to increase casualties dealt, its defensive pips to mitigate casualties received, and its morale pips as well as the fire/shock pips (each for its relevant phase)[2]to increase and mitigate, respectively, morale damage.[5]

The respective effect of pips depends on the shock and fire modifiers of military technology and ideas.

Once artillery becomes prevalent on the battlefield, defensive pips are to be prioritized over offensive pips for infantry and cavalry because artillery can deal damage from the back row. Thus the defensive pips of the frontline regiments impact the kill casualty equation of two enemy regiments, while the offensive pips only affect a single regiment. On the other hand, since artillery on the back row transfers half of its defensive pips (rounded down) to the unit directly in front of it, one could rely on defensive artillery units for protection and prioritize offensive power for one's frontline units instead.

Morale defensive pips are of importance, because morale pips affect both fire and shock phases. However, they only affect morale damage while shock and fire pips affect both strength and morale damage in their respective phase. Priority between fire and shock pips is to be given according to military technology (fire gradually becoming more prevalent as  military technology advances, as a rule of thumb from tech 16 when artillery receive a full+1fire bonus and potentially earlier).

Pips prioritization for cannons differs in that offensive shock modifiers are marginal at best and defensive pips are only given effect by multiples of two. The latter is caused by the defensive pips of cannons being divided by two, then rounded down and ultimately added to the frontline’s defensive pips (or, stated alternatively, contributing half of their defensive pips to the front line). The actual effect is more complex, however, since defensive fire and shock pips both contribute to protection from morale damage during their respective phase,[6]so even an odd number of fire/shocks pips can be useful if the number of morale pips is likewise odd.

#### Flanking range[edit|edit source]

Flanking range determines the horizontal range in which a unit may make a flanking attack. The base flanking range is 1 for infantry, and 2 for cavalry and artillery. There are military technologies which increase the flanking range of units as the game progresses.

Below is a table with said military technology levels and how much they cumulatively increase flanking range.

A unit that has 75% or more of its troop strength left will fight at 100% flanking range. If they are in between 50 and 75% of their strength, they will fight at 75% flanking range. When between 25 and 50% strength they will fight at 50% of their flanking range.

The final range is always rounded down to the nearest integer.

Several ideas give increased cavalry flanking range:

- Albanian idea 4: Hit and Run
- Clanricarde idea 4: Irish Hobbies
- Deccani Sultanate idea 5: Bargi Giri
- Lan Na idea 6: Elephant Charge
- Mossi idea 2: Cavalry Raids
- Najdi idea 5: Arabian Horsemanship
- Ilkhanid ambition
- Kazani ambition
- Horde-Espionage: Psychological Warfare
- Arabian idea 2: Arabian Horses
- Oyo idea 5: The Oyo Cavalry
- +20%Assimilating Evenki culture group asMughals
#### Morale[edit|edit source]

Morale is an important factor in fighting battles. Each day of combat a unit will take a morale hit equal to 1% of the average max morale of enemy troops, regardless of damage taken from an enemy regiment. If it is taking casualties from an enemy, additional morale damage will be inflicted. Once an army's overall morale value has been reduced to zero the army will attempt to retreat. Retreat cannot happen until both two fire and two shock phases have been completed. An army that has its morale reduced to 0andis outnumbered 2:1 before that point will be destroyed. This destruction is known as a stackwipe. Contrary to popular belief, reducing the enemy army to 0 morale before they can retreat isnotsufficient to stackwipe. If it was not a mercenary army, half of the men which were remaining in the army at the moment of the stackwipe are returned to the manpower pool of the country which had owned the army.

A unit that has its morale drop below 0.50 is flagged as disorganized, which is indicated by a small flame next to its morale bar on the map and interface. A disorganized army is unable to start moving until its morale has recovered above 0.50. Newly trained regiments at low land unit maintenance will often fall below this threshold.

If an army loses a battle while having low enough morale to be disorganized, they will be forced to retreat to a controlled province (owned, allied in war, or occupied by player or allies). This province can be very far away from where the battle took place. They will prioritize to retreat to a province with high development, a fort, and no adjacent enemies. While retreating, it cannot be engaged in combat or controlled until it reaches the safer province (or in extreme circumstances if it recovers to 100% morale before reaching the destination). The army also moves slightly faster, and will recover morale at a normal rate during the retreat. If there are no available controlled provinces to retreat to within a large range, the army will shattered retreat to one province away. The army can then be immediately re-engaged, often with very low to even no morale, if a monthly tick has not yet completed. This can be devastating as it is very likely to be stack-wiped if re-engaged immediately.

A controlled retreat is manually ordering an army to retreat from battle after the initial fire and shock phases, and while it still has greater than 0.50 average morale.  This allows the player to control the destination of the shattered retreat. If the morale of an army is less than 0.50 the player can not control the destination. If multiple armies have converged into a battle, it is possible that some armies will have enough morale for a controlled retreat, while others may not (often the initial stack in the battle).

Winning a battle gives the winning armies 50% of their maximum morale and retreating from a battle will reduce the other allied armies' morale relative to the portion of troops leaving the engagement.

After a battle is fought, an army must spend time without fighting for its morale to recover. The normal morale recovery on the 1st of every month cannot occur while in combat.

- A shattered army will get an extra morale bonus once it stops retreating.
- Morale is not recovered whileforced marching.
##### Modifiers[edit|edit source]

The following modifiers contribute to the maximum morale of a nation's army:

- Army maintenance: Ranging from0.51at minimum maintenance to the defined maximum at maximum maintenance.
- Ideas and policies:
- Prussian idea 3: Army Professionalism
- Sundanese ambition
- Andalusian traditions
- Cascadian traditions
- Castilian traditions
- Eranian traditions
- Jerusalem traditions
- Nagpuri traditions
- Norse traditions
- Persian traditions
- Spanish traditions
- Defensive idea 2: Military Drill
- Air idea 2: Cross of Agades
- Balinese idea 5: Conquerer Dalems
- Cirebonese idea 3: Ali's Panther
- Eora idea 6: Pemulwuy
- French idea 2: Lessons of the Hundred Years' War
- Great Qing idea 7: The Ten Great Campaigns
- Highlander idea 1: The Wallace
- Holy Roman idea 2: Kaiserliche Armee
- Iroquoian Federation idea 5: The Good Word
- Kiwi idea 6: Rejecting the Australia Constitution
- Lotharingian idea 2: Glory of Charlemagne
- Muskogean Federation idea 4: Valiant in War
- Polish idea 7: Focus on Field Defenses
- Revolutionary French idea 2: Elan!
- Siouan Federation idea 6: Until Death and After
- Vermont idea 1: Home of the American Revolution
- Veronese idea 4: Civil Blood and Civil Hands
- Zulu idea 5: Warrior Culture
- Manchu ambition
- Swabian ambition
- Texan ambition
- Anhalt traditions
- Aq Qoyunlu traditions
- Augsburger traditions
- Austrian traditions
- Austro-Hungarian traditions
- Ava traditions
- Beninese traditions
- Berber traditions
- Bruneian traditions
- Burgundian traditions
- Butua traditions
- Chernihiv traditions
- Client State traditions
- Corsican traditions
- Dalmatian traditions
- Deccani traditions
- Dhundhari traditions
- Dithmarscher traditions
- Gond traditions
- Hatakeyama traditions
- Hojo traditions
- Huron traditions
- Irish traditions
- Jurchen traditions
- Kamilaroi traditions
- Khorasani traditions
- Korean traditions
- Liège traditions
- Malayan traditions
- Moldavian traditions
- Mysorean traditions
- Nepalese Princedom traditions
- North Western Native traditions
- Oda traditions
- Ogasawara traditions
- Palawa traditions
- Pomeranian traditions
- Provençal traditions
- Punjabi traditions
- Rajputana traditions
- Rothenburg traditions
- Rûmi traditions
- Siamese traditions
- Sicilian traditions
- Somalian traditions
- Transoxianian traditions
- Trent traditions
- Tsutsui traditions
- Welsh traditions
- Zimbabwe traditions
- Indigenous idea 4: Braves
- Plutocratic idea 2: Abolished Serfdom
- Adalite idea 6: Yahu Yahu
- Ajami idea 3: Legacy of the Ilkhans
- Amago idea 4: Ten Brave Warriors
- American Southwest idea 3: Raiding Nomads
- American idea 4: Lessons of Valley Forge
- Aragonese idea 7: Protect the Little Folk
- Ardabili idea 1: The Safavid Order
- Aymaran idea 5: The Tinku Rites
- Aztec idea 4: Eagles and Jaguars
- Bolognese idea 1: Etruscan Origins
- Brandenburg idea 4: Pomeranian Wars
- Bulgarian idea 6: Military Flexibility
- Carib idea 3: Resistance towards the Pailanti'po
- Catalan idea 6: 'Lliures o Morts'
- Cebu idea 1: Lumaya’s Ambition
- Chachapoyan idea 1: Warriors of the Clouds
- Charruan idea 6: Garra Charrua
- Cherokee idea 5: Ghigau
- Chiba idea 2: Dream of Masakado
- Creek idea 7: Red Sticks
- Daimyo idea 4: The Five Rings
- Desmondian idea 3: Gaelic Bastion
- Fijian idea 5: Fijian Warlords
- Finnish idea 7: The Anjala Conspiracy
- French Ducal idea 7: La Petite Nation
- Frisian idea 3: Dutch Courage
- Fulani Jihad idea 4: Imams and Emirs
- Galician idea 5: Santiago y Cierra!
- Garhwali idea 3: Martial Diplomacy
- Gelre idea 5: The Gelderland Wars
- Genevan idea 7: Armed Neutrality
- Goslar idea 6: Resisting the Welfs
- Great Shun idea 4: Obedient to Heaven
- Great Yuan idea 2: A Savage Kingdom Holy and Enchanted
- Herzegovinian idea 3: Stjepan's Rebellion
- Hisn Kayfan (Ayyubid) idea 3: Righteousness of the Faith
- Hisn Kayfan idea 3: Righteousness of the Faith
- Imerina idea 2: The Twelve Sampys of Imerina
- Ionian idea 1: Frankokratia
- Israeli idea 7: The Chosen People
- Iwi idea 4: Kapa Haka
- K'iche idea 6: K'iq'ab's Vengeance
- Kangra idea 3: Martial Heritage
- Khmer idea 1: Preah Ko Preah Keo
- Kikuchi idea 4: Fortify the Domain
- Kildarean idea 3: Silken Thomas
- Krakowian idea 1: Legendary Legacy
- Lanfang idea 4: National Militia
- Livonian idea 2: Border between East and West
- Luban idea 4: Encourage the Kasala Tradition
- Lur idea 6: Rise of the Lurs
- Lüneburger idea 7: Lionhearted
- Mainzian idea 3: Weck, Worscht & Woi
- Majapahit idea 5: Gajah Mada's Oath
- Manipur idea 2: Martial Traditions
- Mayan idea 7: Caste War
- Medri Bahri idea 5: Independent Traditions
- Mexican idea 7: Grito de Dolores
- Miao idea 3: Unity of the tribes
- Mindanao idea 6: Guerrilla Warfare
- Muscovite idea 4: Pomestnoe Voisko
- Mushasha idea 1: Fervent Millenarianism
- Nanbu idea 1: Genji in the North
- Native idea 1: Counting Coups
- Neapolitan idea 4: Crush the Power of the Barons
- Nepali idea 5: The Royal Kumari
- Nivernais idea 4: True Frenchmen
- Northeastern Woodlands idea 5: Marten Clan
- Orleanaise idea 2: The Maid of Orleans
- Pegu idea 4: Ramannadesa
- Perugian idea 6: The War of the Eight Saints
- Rassid idea 1: The Living Imam
- Sadiyan idea 1: Land of Glory
- Saluzzo idea 3: Marquisate
- Samtskhe idea 4: Independent Ambitions
- Sardinian idea 1: From the Judicate
- Semien idea 1: Legacy of Queen Judith
- Serbian idea 7: Balkan Hajduks
- Shiba idea 4: Atsuta Shrine
- Shimazu idea 1: Satsuma Hayato
- Shoni idea 2: Defender of Japan
- Slovak idea 7: Slovak National Awakening
- Songhai idea 3: Jihad Against the Pagans
- Swabian City-State idea 3: Bavarian Resistance
- Takeda idea 1: Leader of Kai Genji
- Three Leagues idea 4: The League of Ten
- Timurid idea 2: The Mantle of the Great Khan
- Tiwi idea 6: Tiwi Isolationism
- Tokugawa idea 1: Mikawa Bushi
- Trebizond idea 5: The Lessons of the Fourth Crusade
- Uesugi idea 4: Dragon of Echigo
- Yarkandi idea 5: Holy Warriors
- Yi idea 7: Children of the Black Tiger
- Ajuuraan ambition
- Athenian ambition
- Brabant ambition
- Circassian ambition
- Colonial ambition
- Cornish ambition
- Dai Viet ambition
- Frankfurter ambition
- Kievan ambition
- Kitabatake ambition
- Pueblo ambition
- Ryazan ambition
- Divine-Religious: Wielders of the Flaming Sword
- Indigenous-Exploration: War on Our Terms
- Mercenary-Religious: Dutiful Mercenaries Act
- Religious-Quantity: Field Priests and Soldier's Prayer Books
- Chagatai idea 2: Ceaseless Border Wars
- Russian idea 7: Broaden the curriculum of the Cadet Corps
- Horde-Influence: Kharash
- Indigenous-Economic: The Three Sisters
- Researching military technology:Military technology (0):+2.0Military technology (3):+0.5(cumulative+2.5)Military technology (4):+0.5(cumulative+3.0)Military technology (15):+1.0(cumulative+4.0)Military technology (26):+1.0(cumulative+5.0)Military technology (30):+1.0(cumulative+6.0)
- Military technology (0):+2.0
- Military technology (3):+0.5(cumulative+2.5)
- Military technology (4):+0.5(cumulative+3.0)
- Military technology (15):+1.0(cumulative+4.0)
- Military technology (26):+1.0(cumulative+5.0)
- Military technology (30):+1.0(cumulative+6.0)
Various national bonuses:

- Prestige:+10%at 100 prestige,-10%at -100 prestige
- Power projection:+10%at 100 power projection
- Army reformer advisor:+10%
- Army tradition:+25%at 100 tradition
- Being theDefender of the Faith:+5%(only at tier 3 or higher withEmperor)
- Piety (Muslim only):+10%at 100 mysticism
- Golden Era:+10%
Religion:

- Shia:+5%
- Protestant church aspect ‘Saints Accept Prayers’:+5%
- Reformed "War" focus (requiresWealth of Nations DLC)+10%
- Catholic during acrusade:+10%
- Catholic with bless ruler curia power+10%
- Vajrayana:+5%
- Shinto:+10%
- Sikh:+10%
- Inti with ‘Yana Lords’ reform:+10%
- Nahuatl:+10%
- Tengri with either Shia, Nahuatl or Sikh as syncretic faiths:+5%
Government:

- Noble Republic:+10%
- Revolutionary Empire:+10%
- Daimyo:+10%
- Merchant Republic with "Aristocrats" Faction in power:+5%
- Republican Dictatorship:+10%
- Revolutionary Republic:+10%
- Ambrosian Republic:+5%
- Peasants Republic:+5%
- Assimilating Japanese culture group asMughals:+10%
##### Morale recovery[edit|edit source]

Every month, a regiment recovers 15% of its maximum morale. The following contributes to a nation's morale recovery speed.

- Regiment is in home territory:+5%
- Army tradition:+10%at 100 tradition
- When commanded by a leader with the Inspirational Leaderpersonalitytrait:+10%
- Various events, decisions, and modifiers
- Armies that win battles will gain a significant boost to morale, to prevent situations where an army is stack wiped due to winning a narrowly fought battle and then immediately being attacked. The amount of morale regained depends on the strength of the enemy army defeated relative to their own strength.
- Certain ideas and policies as follows
- Expansion-Defensive: Local Army Organization
- Mercenary-Expansion: Hired Expeditions Act
- Quality-Administrative: The Liquor Act
- Armenian traditions
- Fulani traditions
- Great Armenian traditions
- Montferrat traditions
- Ryazan traditions
- Pskovian idea 2: Legacy of Daumantas
- Fully Offensive
- Persian ambition
- Divine-Administrative: Omne Datum Optimum
- Religious-Quantity: Field Priests and Soldier's Prayer Books
#### Cavalry to infantry ratio[edit|edit source]

The country'scavalry to infantry ratio shows what percentage of the front line can be made up of cavalry. Having the front line be made up of more cavalry than the country's ratio allows applies the"insufficient support"penalty, which is amilitary tactics malus to cavalry regiments equal to the percentage by which the ratio is exceeded, divided by 2. In steppes this malus is doubled. For example, if the ratio is 50%, but the front line is made up of 100% cavalry, these units will receive a−25%military tactics malus, which is raised to−50%in steppes. This ratio threshold is checked daily even during battles, and is based on the actual headcount of individual soldiers instead of regiments. Since infantry tends to take more casualties than cavalry, it is advisable to take at least a bit more infantry than the ratio would suggest, and (to maximize the number of cavalry used, since deployment prioritises infantry) reinforce the battle with fresh infantry as regiments retreat.

The basecavalry to infantry ratio is50%. This is further modified by the following:

- Epirote idea 5: Latin Knights
- Hisn Kayfan (Ayyubid) idea 4: Elite Warriors
- Latin idea 5: Latin Knights
- United Arabian idea 1: Arabian Horseman Tactics
- Hungarian ambition
- Lan Xang traditions
- Aristocratic idea 3: Noble Connections
- Horde government idea 1: Horse-lords of the Steppes
- Plains Native idea 7: Horse Riders
- +50%Great Mongol State government
- +50%Reward fromTeutonic OrderCrusader path missionEstablish a Great Cavalry, upgraded from+25%or+10%from previous mission rewards on the Crusader path.
- +50%Possible reward fromCommonwealtheventExpanding the Quarter Armyprovided specified conditions are met.
- +50%Legacy of the Seljuktier 5 government reform
- +25%Steppe Horde government
- +25%Tengri (withnosyncretic faith)
- +25%All Under Tengrigovernment reform
- +25%Employ the Cuman Lancerstier 5 government reform (available toHungaryorAustria-Hungary)
- +20%Reward fromLan XangmissionA Million Elephants
- +20%Cavalry Armies ability (anAge of Discovery only ability)
- +25%Sich Radagovernment reform (available toZaporozhieor anyCossack Breakaway)
- +10%Cavalry Warfaretier 5 government reform
- +10%Compagnie d'ordonnancetier 5 government reform (available to French culture group)
- +10%Celestial reform Popularize the Banners asEmperor of China
- +10%Sunni
- +10%LoyalCossacks estate (max value)
### Forts[edit|edit source]

Forts are used to protect a nation from invading armies.

#### Fort level and garrison[edit|edit source]

The following modifiers affect fort level:

- Capital province:+1fort level for thecapital province
- Fort buildings:+2fort level per building level.
Each fort level increases the garrison of the province by 1000 and provides a−1modifier to the besieger's siege rolls. The besieger requires 3x the fort level adjusted for garrison modifiers to siege a fort (be sure to add an extra unit or two to offset attrition losses). Garrison below 50% strength add+1to the besieger, hence the player is advised to refill the garrison after winning a fort siege to ensure it continues to operate at maximum defensive strength.

Maximum garrison size is also increased by the following ideas and policies:

- Defensive idea 7: Improved Foraging
- Desmondian traditions
- Highlander traditions
- Isshiki traditions
- Great Ming idea 1: Nine Garrisons of The Great Wall
- Toki idea 4: Strategic Castles
- Trading City idea 2: Walls of the City
- Infrastructure-Defensive: Bolstered Defence Act
- Nuremberger traditions
- Bayreuther idea 3: Plassenburg
- Betsimisaraka idea 1: People of the Coast
- Cilli idea 5: Border Wars
- Dortmund idea 6: Fortmund
- Eranian idea 6: Rebuild the Caspian Gates
- Rothenburg idea 7: Klingentorturm
- Innovative-Quantity: The Garrison System
- Divine idea 5: Onward Christian Soldiers
- Garhwali idea 2: Himalayan Kingdom
- Italian (minor) idea 4: Trace Italienne
- Kangra idea 4: Control of the Hill Forts
- Slovak idea 4: Land of Castles
- Indigenous-Humanist: By the People, for the People
Unless the province is besieged, the garrison recovers monthly at a base rate of5%plus:

The rate is also increased by the following national ideas and policies:

- Ito traditions
- Luxembourg traditions
- Meath traditions
- Pueblo traditions
- Rigan traditions
- Clevian idea 7: Militarize Schwanenburg
- Toki traditions
- Austrian idea 2: Military Frontier
- Divine idea 5: Onward Christian Soldiers
#### Fort maintenance[edit|edit source]

Each building level of fort costs1 ducat per month. Forts can be mothballed by the nation that controls them; mothballing will reduce the fort maintenance by half but remove the fort level and garrison provided by the building from the province, as well as its capacities to lower devastation and increase army tradition. A fort cannot be mothballed or de-mothballed while the province is under siege. The garrison will recover at a normal rate after mothballing is cancelled. Capital provinces always have fort level at least 1, with a corresponding base garrison of 1000, which stacks with any fort building in the province; this free fort level does not extend a zone of control (though does still reduce devastation as a normal fort would), does not cost maintenance, and cannot be mothballed. A fort building in a capital province can be mothballed as normal, but the free fort will remain.

Mothballed or not, fort maintenance can be reduced by following modifiers:

- with ‘Monastic Order’government reform.
- with ‘Grant Noble Castle Rights’ government reform.
- with ‘Sidhi Recruitment’ government reform.
- withparliament and active issue ‘Tax Provinces for Fortifications’.
- asmarch.
- Innovative-Defensive: Superior Fortifications
- Infrastructure idea 6: Fortification Logistics
- Bukharan idea 5: The Ark
- Innovative-Quantity: The Garrison System
- Great Ming traditions
- Lur traditions
- Mantuan traditions
- Meath traditions
- Vindhyan traditions
- Cascadian idea 3: The Forts of Hudson Bay
- Estonian idea 3: Castles of Estonia
- Ladakh idea 2: Fortified Mountain Cities
- Muscovite idea 6: Zasechnaya Cherta
- Odoyev idea 6: Fortification Efforts
- Somali idea 2: Qalqads
- Swiss idea 4: Alpine Defensiveness
- Sligonian ambition
- Garjati traditions
- Gujarati Princedom traditions
- Banteni idea 4: Rebuttal
- Bolognese idea 6: La Turrita
- Livonian Knight idea 3: Castles of the Order
- Luxembourg idea 4: The Fortress of Luxembourg
- Northumbrian idea 4: A Land of Castles
- Telugu idea 4: Great Forts of the East
- Baden traditions
- Baluch traditions
- French Ducal traditions
- Miao traditions
- Nizhny Novgorod traditions
- Zimbabwe traditions
- Defensive idea 5: Defensive Mentality
- Ajami idea 5: Tribes of Iraq-e Ajam
- Austrian idea 2: Military Frontier
- Catalan idea 4: Fortifying Catalonia
- Iwi idea 5: Pa Defense
- Kangra idea 4: Control of the Hill Forts
- Laotian idea 7: Laotian Hill Warfare
- Mutapan idea 3: Mutapa Architecture
- Nubian (minor) idea 7: Fortified Strongholds
- Purépecha idea 5: Fortified Frontier
- Semien idea 2: Mountain Kingdom
- Slovak idea 4: Land of Castles
Fort maintenance is capped at-90%.

On Provinces that border a rival, fort maintenance is further modified by the "Fort maintenance on Border with Rival" modifiers. These are applied multiplicatively onto the usual fort maintenance, and cap at-100%.

- Religious-Plutocratic: The Tolerance Act
- Andalusian idea 7: Al Awasim
- Veronese idea 3: Ancient Grudge
#### Zone of control[edit|edit source]

Active fort buildings (not counting the free fort level in the capital) provide a zone of control. A zone of control restricts the movement of enemy armies through the province with the fort, and provinces immediately adjacent to it. When an army enters a zone of control from a province not affected by a hostile zone of control the province it entered from is set as the 'return province'. In general the army can then only move to another province that has no more than one province that is not affected by a hostile zone of control between itself and the return province. The main exception to this rule is that the army can always move to a hostile fort. Please see the main article for full details as there are a number of exceptions and the behaviour is not intuitive.

An occupied province that does not have a fort in it but is next to a fort will automatically revert back to its owner's control after about a month.  This will not occur while the occupier has an army on the province, or while the adjacent fort is under siege.

#### Sieges[edit|edit source]

When hostile troops enter a province and stop moving, a siege/occupation will begin. To progress, the attacker requires a minimum of 3000 men per 1000 garrison. If the province has no garrison (whether because it has no fort or the fort's garrison is empty), 1000 men is enough and occupation is guaranteed within a month. Any unit types can be used for sieging, but for sieging a fortified province, only infantry will be used in anassault, and artilleryspeeds the siege up. Progress in a siege will never decrease as long as attackers are continuously present; however, if all attackers leave the province, you will lose 1 siege status progress per day the province is unsieged.

Besieging armies will always take at least1%baseattrition, even if the province is unfortified. This rule only applies to enemy-owned provinces, however - when besieging friendly provinces to retake them from the enemy, this rule is ignored.

An army besieging a fort always count as the attacker if a battle takes place and will receive theattacker penalty.

A siege ends successfully either when surrender is obtained through dice roll or when a siege tick finishes while the garrison is below 100 men.

##### Sortie[edit|edit source]

The garrison can be ordered to make a sortie to fight the hostile army, at the cost of10military power. (The‘Sortie from siege’ button is shown on the siege screen.) If the garrison army, which consists only of infantry, loses the fight, the province and fort will become occupied. Since sortie-ing troops fight together with friendly stacks if there are ones, this can be used to win a battle in which both sides are evenly matched. Sortie can be ordered only when siege is ongoing, thus friendly troops awaiting an inbound enemy in a fortified province cannot receive garrison's aid.

Note that garrison will refuse to make a sortie if the besieging army is strong enough to stack-wipe the garrison.

##### Siege ability[edit|edit source]

Siege ability is influenced by the following ideas and policies:

- Offensive idea 5: Engineer Corps
- Arabian ambitions
- Revolutionary French ambitions
- Ferraran traditions
- Jolof traditions
- Saxe-Lauenburg traditions
- Espionage idea 3: Efficient Spies
- Beninese idea 2: Isiatua
- Dutch idea 6: Army Sappers
- Great Shun idea 5: Perfection of Siegecraft
- Highlander idea 3: Storming the Castle
- Ormond idea 6: Irish Siegecraft
- Otomo idea 7: Kunikuzushi
- Smolenskian idea 7: Tsar Mortars
- United Crowns idea 5: Army Sappers
- Utrecht idea 3: Fortified City
- Luxembourg ambition
- Divine-Espionage: My Word Is My Bond
- Horde-Diplomatic: Fear Tactics
- Innovative-Offensive: Modern Siege Weapons
- Quality-Religious: The Military Zeal Act
Various modifiers:

- War exhaustion:−1%per point
- Army Tradition:+5%at 100
- Spy network:+20%at 100(RequiresMare Nostrum)
- Tengri withCoptic syncretic faith:+10%(RequiresThe Cossacks)
- Hindu withShakti as divinity:+5%(RequiresWealth of Nations)
- Army professionalism:+20%at 100(RequiresCradle of Civilization)
- Improve inland routes trade policy:+10%(RequiresCradle of Civilization)
- General withSiege Specialistpersonality:+15%
- Military Hegemonat max hegemon power:+20%(RequiresEmperor)
- Lucky nation(AI only):+5%
##### Fort defense[edit|edit source]

Fort defense is influenced by the following ideas and policies:

- Georgian traditions
- Rothenburg traditions
- Defensive idea 5: Defensive Mentality
- Afghan idea 2: Shadows of the Hindu Kush
- Bregenzer idea 6: In the Shadow of Pfander
- Bremen idea 6: Bremish Walls
- Cypriot idea 5: Cypriot Fortifications
- Divine idea 3: True Defender of the Faith
- Genevan idea 6: Unconquerable City
- Hamburger idea 3: Walls of Hamburg
- Jerusalem idea 6: Crusader Castles
- Knights Hospitaller idea 1: Defense of the Faith
- Mainzian idea 6: The Guard of the Rhine
- Sardinian-Piedmontese idea 2: Defensive Prowess
- Swiss idea 4: Alpine Defensiveness
- Theodoro idea 5: Mangup and Kalamita Forts
- Ulmer idea 4: Dürer's Fortifications
- Zimbabwe idea 4: Zimbabwe's Walls
- Indigenous-Humanist: By the People, for the People
- Albanian traditions
- Bolognese traditions
- Circassian traditions
- Kildarean traditions
- Leinster traditions
- Mushasha traditions
- Odoyev traditions
- Orleanaise traditions
- Ormond traditions
- Slovak traditions
- Telugu traditions
- Tsutsui traditions
- Wallachian traditions
- Yi traditions
- Ainu idea 1: Chasi
- Ajami idea 1: Jibal
- Al-Haasa idea 4: Fortify the coastline
- Barbary Corsair idea 5: Fortified Pirate Strongholds
- Breton idea 3: Breton March
- Caspian idea 6: A Safe Haven
- Chickasaw idea 6: Lessons of Ackia
- Couronian idea 1: Legacy of Sword Brethren
- Dai Viet idea 3: Autonomous Villages
- Dhundhari idea 1: Improve the Fort at Amer
- Dortmund idea 6: Fortmund
- Eranian idea 6: Rebuild the Caspian Gates
- Ethiopian idea 3: Hostile Borders
- Franconian idea 3: A Rugged Land of Fortresses
- Galician idea 2: Galicia la Bella
- Hisn Kayfan (Ayyubid) idea 1: Citadels and Fortresses
- Hisn Kayfan idea 1: Citadels and Fortresses
- Hojo idea 5: Castles of the Hojo
- Hormuz idea 2: Protecting the Islands
- Horn of African idea 7: Defensive Nature
- Ionian idea 2: Castles of the Angels
- Ito idea 5: Network of Forty-Eight Fortifications
- Krakowian idea 4: Casimirian Fortifications
- Latgalian idea 5: Modernize Livonian Castles
- Ligori idea 5: Bridge to Siam
- Lorraine idea 1: The Vosges
- Luxembourg idea 2: The Ardennes
- Malvi idea 4: Fortified Strongholds
- Mantuan idea 4: Gonzaga's Walls
- Maratha idea 2: Forts of Maharashtra
- Mazovian idea 2: Mazovian Frontier
- Meath idea 7: Siege Mentality
- Mindanao idea 5: Fortify our Ports
- Nivernais idea 5: Bridges of the Loire
- Offaly idea 5: Tower Houses
- Ogasawara idea 1: Shinano Shugo
- Perugian idea 1: Saint Herculanus
- Rigan idea 6: Fortify Riga
- Samtskhe idea 3: Fortresses of Samtskhe
- Savoyard idea 1: Repel the French
- Shirvani idea 2: Fortresses of Shirvan
- Sundanese idea 3: Defensive Moats
- Swabian City-State idea 2: By the River Iller
- Thüringian idea 2: Fortifications of Erfurt
- Trebizond idea 2: Pontic Mountains
- Tripuran idea 7: Strengthen Local Defenses
- Tverian idea 2: Defend Against Muscovy
- Tyrconnell idea 1: Fort of the Foreigners
- Ulster idea 7: Last Redoubt of Ireland
- Yamana idea 6: Isolated Heartland
- Italian ambition
- Ladakh ambition
- Mesoamerican ambition
- Novgorodian ambition
- Permian ambition
- Rassid ambition
- Sumatran ambition
- Aymaran traditions
- Carib traditions
- Kurdish traditions
- Mayan traditions
- Montenegrin traditions
- Muiscan traditions
- Transylvanian traditions
- Amago idea 3: Fortified Strongholds
- American Southwest idea 5: The Grand Canyon
- Bosnian idea 7: Over the Hills and Through the Woods
- Byzantine idea 5: Protect the Frontiers
- Chernihiv idea 4: Konotop Fortress
- Clevian idea 1: Walled Cities
- Client State idea 3: Fortified Border
- Danziger idea 6: Continued Independence
- Ferraran idea 6: Este Castle
- Finnish idea 1: Expand Viborg
- French idea 7: Vauban Fortifications
- Frisian idea 5: Flooding the Polders
- Fulani Jihad idea 2: Unrighteous Kings
- Garjati idea 1: Securing Our Defenses
- Gond idea 1: Securing Our Defenses
- Guarani idea 6: Repel the Bandeirantes!
- Imerina idea 4: Fortify the Highlands
- Iroquoian Federation idea 2: Tree of Peace
- Kazani idea 6: Settle Down
- Khivan idea 6: Ichan Qal'a
- Kievan idea 3: Fending Off The Invaders
- Kikuchi idea 7: Central Stronghold
- Malagasy idea 1: Fortify the Coastline
- Mapuche idea 1: Mapuche Pucaras
- Mewari idea 3: The Fort of Kumbhalgarh
- Mossi idea 5: Land of the Ancestors
- Nepalese Princedom idea 5: Seize the Mountain Passes
- Nepali idea 2: Land of Peaks
- Northeastern Woodlands idea 1: Turtle Clan
- Provençal idea 4: Tarascon Castle
- Pueblo idea 3: Mesa Settlements
- Québécois idea 4: Fortifications of Quebec
- Rajput idea 2: Fortifying Rajputana
- Sadiyan idea 3: Hills and Jungles
- Shan idea 1: Fortified Cities
- Siberian idea 4: Siberian Backwoods
- Siddi idea 3: Impregnable Island Fortress
- Sligonian idea 2: Rebuild the Castle of Sligo
- Songhai idea 2: Independence from Mali
- Teutonic idea 5: Expand the Marches
- Vindhyan idea 2: Forts of the Vindhyas
- Yaroslavlyian idea 6: The Two Towers
- Desmondian ambition
- Manipur ambition
- Espionage-Defensive: The Privy Council Establishment Act
- Mercenary-Espionage: Loyal Conduct Act
- Athenian traditions
- Dahomey traditions
- Pagarruyung traditions
- Pisan traditions
- Sinhalese traditions
- Andalusian idea 7: Al Awasim
- Andean idea 6: Hidden Cities
- Beninese idea 4: The Walls of Benin
- Bornean idea 4: Anti-Piracy Measures
- Chachapoyan idea 3: Summit Fortresses
- Cham idea 7: Resisting Foreign Rule
- Cherokee idea 6: Mountainous Isolation
- Chimu idea 2: Ciudadelas
- Garhwali idea 2: Himalayan Kingdom
- Holstein idea 1: Limes Saxoniae
- Kongolese idea 1: The Kongo River Basin
- Lan Xang idea 6: Merchants of Vientiane
- Nizhny Novgorod idea 4: Citadel Of Russia
- Polotskian idea 4: Land of Strongholds
- Portuguese idea 7: Royal Academy of Fortification, Artillery and Drawing
- Purépecha idea 5: Fortified Frontier
- Tupi idea 7: Wall Builders
- Utrecht idea 3: Fortified City
- Moldavian ambition
- Innovative-Defensive: Superior Fortifications
- Croatian idea 4: Antemurale Christianitatis
- Great Ming idea 1: Nine Garrisons of The Great Wall
- Italian (minor) idea 4: Trace Italienne
- Toki idea 4: Strategic Castles
Various Modifiers:

- Hindu withVishnu as divinity:+20%(RequiresWealth of Nations)
- Norse withTor as divinity:+10%(RequiresEl Doradoor a save converted fromCrusader Kings II)
- Coptic:+15%
- Power Projection:+10%at 100 Power Projection
- Defence Edict:+33%
- Local/Permanent Quarters trade company investment:+15%/+30%
- Ramparts manufactory:+15%
- Earthworknative building:+25%
- Military Engineer advisor:+20%
- Salt production in province:+15%
- Lucky nation (AI only):+10%
- Certaineventscan temporarily increase siege ability or fort defense.
##### Phases[edit|edit source]

A siege progresses in phases. Each phase has a base length of 30 days and is modified by:

- Fort defense: +1% per defender's 1%fort defense andprovince defensiveness (produces salt:15%, hills or highlands terrain:10%, mountain terrain:25%)
- Siege ability: −1% per attacker's 1%Siege Ability
- Tactics difference: 6.25% per 0.25military tactics difference to both sides. E.G. If the player's tactics is 0.5 higher than the enemy, the player's siege will be 12.5% faster and the enemy's siege will be 12.5% slower. Only the base tactics value counts, bonuses from discipline have no effect on phase time.
A siege dice roll is also triggered if the sieging army wins a battle on the besieged province.

The mean number of phases to finish a siege for a particular starting bonus is as follows:

"Sieges per year" is computed at the default phase length of 30 days.

##### Dice roll[edit|edit source]

At the end of each siege phase, a die (1 to 14) is rolled. The following modifiers are then applied:

- Siege status.The most important modifier. As the siege goes on, this bonus will increase from its starting value of 0 depending on previous dice rolls. The maximum starts at 12 for a Castle or capital fort and is increased by 1 for each building level above a Castle, up to a maximum of 15 for a Fortress.
- Leader siege.If the attacking army has a leader, the leader's siege skill (+0–6) is added as a bonus.
- Artillery.Adding artillery to a siege will add a+1to+5besieging Artillerybonus.The game calculates Artillery as follows:Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{artillery}=\frac{\text{Artillery soldiers}\cdot\text{Artillery levels contribution to siege}}{1000} }The base value of Artillery levels contribution to siege is 1. It can be increased by a few bonuses (see below).The artillery soldiers can be in different regiments. Having 10 regiments with 100 artillery each is the same as 1 regiment with 1000.Where multiple countries with different values for Artillery levels contribution to siege are involved, they contribute different amounts to a shared siege.1 artillery will always give at least a+1bonus, regardless of fort level.For higher values:Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{besieging Artillery} = \text{Min}\left(\left \lfloor  \frac{\text{Artillery}}{\text{Fort Level}}\right \rfloor,\text{Artillery Levels Available vs Fort}\right)}For the value of Artillery Levels available vs Fort,see below.
- The game calculates Artillery as follows:Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{artillery}=\frac{\text{Artillery soldiers}\cdot\text{Artillery levels contribution to siege}}{1000} }The base value of Artillery levels contribution to siege is 1. It can be increased by a few bonuses (see below).The artillery soldiers can be in different regiments. Having 10 regiments with 100 artillery each is the same as 1 regiment with 1000.Where multiple countries with different values for Artillery levels contribution to siege are involved, they contribute different amounts to a shared siege.
- The base value of Artillery levels contribution to siege is 1. It can be increased by a few bonuses (see below).
- The artillery soldiers can be in different regiments. Having 10 regiments with 100 artillery each is the same as 1 regiment with 1000.
- Where multiple countries with different values for Artillery levels contribution to siege are involved, they contribute different amounts to a shared siege.
- 1 artillery will always give at least a+1bonus, regardless of fort level.
- For higher values:Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{besieging Artillery} = \text{Min}\left(\left \lfloor  \frac{\text{Artillery}}{\text{Fort Level}}\right \rfloor,\text{Artillery Levels Available vs Fort}\right)}For the value of Artillery Levels available vs Fort,see below.
- For the value of Artillery Levels available vs Fort,see below.
- Blockade.If the province is coastal and not completely blockaded, a−2penalty is applied, or−1if the attacker is the rightful owner of the province. Partial blockades (anything less than 100% for the province in question) have no effect on sieges. Note that the blockading fleet doesn't have to be owned by the same nation as the sieging army, or even a part of the same war to help in a siege. Some bonuses can increase the effect of blockades on sieges;see below.
- Fort level.The defender's fort level is applied as a penalty.Obsolete fort.If the attacker's technology allows the building of more advanced forts, than the sieged one, they gain a+1bonus per fort level difference. A capital without a fort counts as less advanced than a castle.Insufficient garrison.Having less than half of the maximum garrison gives the attacker a+1bonus. If the fort has no garrison whatsoever (i.e., if the fort has been mothballed during this month and is not a capital), then the province is treated as unfortified and the siege will automatically succeed. Below 100 garrison a siege will succeed automatically on the next siege tick, regardless of progress percentage.
- Obsolete fort.If the attacker's technology allows the building of more advanced forts, than the sieged one, they gain a+1bonus per fort level difference. A capital without a fort counts as less advanced than a castle.
- Insufficient garrison.Having less than half of the maximum garrison gives the attacker a+1bonus. If the fort has no garrison whatsoever (i.e., if the fort has been mothballed during this month and is not a capital), then the province is treated as unfortified and the siege will automatically succeed. Below 100 garrison a siege will succeed automatically on the next siege tick, regardless of progress percentage.
- Walls breached.Each time the walls are breached, the breach status value will increase by 1, to a maximum of+3. If this value is at least+1, then the fort can also be assaulted (see below). Rolling for walls breached is calculated separately to the normal siege roll.Without any modifiers, breaching the walls requires you to roll a 14.Each+2bonus from artillery (see table above) adds a+1to the dice roll for breachingExample: With+3bonus from artillery, you would need to roll 13 or 14 to create a breach. With+6artillery bonus, you would need 11 or above.In addition, every+2bonus from having an obsolete fort (see above) adds another+1for breaching.
- Without any modifiers, breaching the walls requires you to roll a 14.
- Each+2bonus from artillery (see table above) adds a+1to the dice roll for breachingExample: With+3bonus from artillery, you would need to roll 13 or 14 to create a breach. With+6artillery bonus, you would need 11 or above.
- Example: With+3bonus from artillery, you would need to roll 13 or 14 to create a breach. With+6artillery bonus, you would need 11 or above.
- In addition, every+2bonus from having an obsolete fort (see above) adds another+1for breaching.
The highest possible starting bonus is+24: a capital fort (−1), obsolete by 3 fort levels (+3), with an insufficient garrison (+1), with a 6-siege general (+6), blockading with a flagship modified with Mortars (+1), Norman ideas: Naval invasion (+1), Naval doctrine: Portuguese Marines (+1), Naval-espionage policy (+1) and at least 11 regiments of artillery (+11). The worst possible starting bonus is−11, for a level 8 fort in a capital (−9) with no blockade (−2).

Artillery levels contribution to siege can be increased by:

- Divine-Espionage: My Word Is My Bond
- Eranian idea 7: Sasanian Siege Warfare
Artillery Levels available vs Fort is by default5. It can be increased by:

- Infrastructure-Offensive: Mobile Siege Engines Act
Blockade impact on siege is affected by:

- Naval idea 4: Naval Glory
- Norman idea 6: Naval Invasion
- Naval-Espionage: The Maritime Intelligencer Unit
- Naval-Maritime: The Naval Supremacy Act
##### Effects[edit|edit source]

The die roll may result in an increase of the siege status, which improves the results of future siege stages. Maximum siege status values goes up with the attackers's maximum fort building level. (12/13/14/15 for fort building level 1/2/3/4). Maximum breach status is always 3.

- If theunmodifiedroll is 1, a Disease Outbreak happens—the attacking army loses 5% of its troops, and the siege does not progress (a surrender takes priority over a Disease Outbreak).
- If a breach occurs, ignore all results on the table below except for "Surrender". If the fort does not surrender, add 1 to the breach status and 2 to the siege status. Artillery barrage and naval barrage breaches work slightly differently (see below)
- Then look up themodifieddie roll on the table below.
The attacker needs at least a net +6 bonus to have a chance of ending the siege.

To be noted that the success rate shown on the screen only reflects the probability of getting the modified die roll ≥ 20, and when the garrison is very low the modified die roll 5-19 might immediately end siege due to loss of garrison.

##### Artillery barrage[edit|edit source]

The option to conduct an artillery barrage becomes available when a siege has at least one full artillery regiment per fort level. This costs50military power and creates 3 breaches in the walls. In total, these add +3 permanent siege status. Rolling a natural breach is still possible and will affect the siege status but will not add another breach. The power cost is affected by modifiers toall power costs and can be further reduced by−25%by thecommon government reform "Military Engineering".

##### Naval barrage[edit|edit source]

Same as artillery barrage, but only available if the number of cannons on ships adjacent to the fort divided by 100 equals the fort level. The base cost is50military power which can be further modified byPortuguese naval doctrineandflagship modification. With both perks on, the cost can be reduced down to10military power. From 1.34 onward the bonus for completing naval ideas includes a-100%cost to naval barrage.

##### Assault[edit|edit source]

The attacker may choose to assault the garrison with their infantry if the walls have been breached at least once. The averagemorale of the besieging infantry needs to be0.5or higher to do so. This can result in a speedy conclusion of the siege at the cost of5military power, and usually costs lots of lives. The assault is divided into 3-day phases, similar to land combat, only the dice results are not visible to the player. The attacker loses roughly 5 times as many troops as defender does and assaults on fully-manned forts are highly discouraged. Only infantry can assault and onlyFailed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle (\text{fort level}\times5000)}men can be part of an assault per day. If all infantry units of the attacker are killed before the defenders are defeated, or the attackers run out of morale, the remaining troops will continue the siege normally. Infantry regiments reduced to 0 men during an assault are not disbanded and can continue a siege on their own, though they are extremely vulnerable to a sortie.

The morale damage dealt to either side in an assault largely depends on the die roll and the received losses.

The losses during an assault depend on the localdefensiveness, which can be decreased by thesiege ability of the attacker and increased byfort defense of the defender.Assault fort ability reduces this value for the purpose of assaults the same way siege ability does, for example Janissary regiments (+50%) assaulting a fort with+50%local defensiveness are as effective as regular Infantry assaulting a fort with0local defensiveness.

Many modifiers helping in regular battles have no effect in assaulting forts, notablymilitary tactics,discipline,//damage dealt,//damage received,infantry combat ability, or even infantry unit pips. Onlyinfantry shock from technology has an effect;infantry shock from national ideas andinfantry fire from either source do not. Highermorale of armies does allow your troops to assault and your garrison to resist assaults longer, but does not increase morale damage dealt.

Higher fort levels are only harder to assault in the sense that the garrison is greater: a fully garrisoned level 3 fort with+33%garrison size is harder to successfully assault than a fully garrisoned level 4 fort; both have 4000 garrison but more infantry can be part in the higher level fort's assault.

### Mechanics of an army[edit|edit source]

#### Exile[edit|edit source]

An exiled army can be identified by a black flag attached to its unit icon. It can't fight, siege provinces or explore, and it won't lift fog of war even in the province it's in. However, it can traverse any territory (other than wasteland) without needing military access. It still suffers attrition and its regiments can still move between armies, though regiments can't be mixed between exiled and non-exiled armies.

An army will become exiled under the following circumstances:

- When a war ends, any army still in territory it doesn't have peacetime access to is exiled. This prevents it from being permanently stuck in a place it can't get out of, as well as preventing several exploits.
- When a war begins, any army in a neutral or hostile province that it only had access to through a military access agreement is exiled. This prevents troops from being placed outside their country's territory in preparation for war. An army in uncolonized land or the territory of a subject or ally won't be exiled, even if the ally isn't called into the war.
- When anative tribemigrates, any armies that happen to be in the province it migrated to at the time and don't otherwise have access are exiled.
- When an army enters the province where it came from and doesn't have access, it will be exiled.
- When an army is in a province to which it lost military access in any other way it will also be exiled.
It will stop being exiled when it either:

- enters a province that the army's country or one of their subjects control or own (butnotthe overlord's provinces for a subject country). This includes home provinces occupied by an enemy.
- boards a transport ship that moves into a sea zone or is currently in one.
If an army is in combat when it gets exiled, the battle will end only if all of its enemies are no longer hostile. For example, if an army is fighting rebels in enemy territory when peace is signed, they will continue fighting despite being exiled.

#### Looting[edit|edit source]

Every traversable land province (other than developing colonies and uncolonized provinces) has a loot bar. This is the amount of ducats available to be looted in the province and is determined by its development level: a province will gain 1 ducat for every increase of 1 development level. An army standing in a province owned by an enemy (regardless of who controls it) during a month tick will loot the province if any loot is available. The amount of loot taken depends on the number and type of troops in the province. A full strength infantry/cavalry/artillery regiment loots 0.1/0.3/0.05 ducats per month,[7]those ducats being taken directly out of the besieged country's treasury. The money appears on theeconomytab as "Spoils of War" for the looting country and "Diplomatic Expenses" for the province owner. When a province's loot bar is empty no more loot can be taken from that province. A province will only begin to recover two years after the last successful looting, at a rate of 10% each month.

A coastal raidin contrast loots every available ducat at once, but does not take it out of the raided country's treasury.

Looting is the main cause ofdevastation, which greatly reduces the owner's production income and manpower, as well as decreasing movement speed, supply limits andinstitutionspread. Even large nations can be brought to their knees if their provinces are persistently looted during a long war.

Various ideas increaselooting speed; this bonus increases the amount ofducats looted each month by the stated amount (and thus decreases the time taken to fully loot a province).

- Ashanti traditions
- Baluch traditions
- Cossack traditions
- Interlacustrine traditions
- Manipur traditions
- Zaporozhian traditions
- Crimean idea 3: Lead Raids into Ruthenia
- Gelre idea 6: Loot as Payment
- Piratical idea 2: Plunder!
- West African traditions
- Anatolian idea 3: Akîncî Cavalry
- Berber idea 5: Tuareg Cavalry
- Chickasaw idea 5: Slave Raids
- Shan idea 5: Raiders
- +50%Assimilating Great Lakes culture group asMughals
Some bonuses increase the loot available in foreign provinces

#### Attach to army[edit|edit source]

This action attaches the player's army to a friendly army, causing their army to travel and fight alongside the friendly unit without further input from the player. The army can be detached at any time except in battle. An attached army cannot board transports. Attaching units to an AI army will change its behavior, making it bolder and more willing to actively engage enemies.

#### Attack natives[edit|edit source]

The native population of a colony or uncolonized province can be eliminated using theattack nativesmilitary action. A native army equal in size to the local native population (rounded to the nearest thousand) will spawn immediately and must be defeated in battle to clear out the native population. This action costsmilitary power proportional to the native population,aggressiveness, andferocity, and will permanently reduce the potential value of the province from the native assimilation bonus. The elimination of all natives in a province will prevent any future raids on the local colony or any passing armies.

#### Scorched earth[edit|edit source]

An army in an owned and controlled province may scorch the earth for5military power, as long as it has not already been scorched. This increasesdevastationin the province by10and gives the province modifier“Scorched Earth”, lasting for 60 months with the following effects:[8]

The devastation itself has the following effects (scaled to these figures at 100 devastation), decaying as devastation decays as usual:

Scorching the earth can be useful when the player's army is too weak to fend off attackers and their provinces are likely to be occupied. It increases attrition (hurting the enemy's manpower), and makes the provinces less valuable to the attacker while they're occupying them. The player will lose income in the meantime, but if they were going to lose control of them anyway it could be a good idea to make them less valuable for the enemy.

#### Rebel suppression[edit|edit source]

Stationing an army in an allied province provides a “Friendly Troops” negative modifier to unrest in that province, to the value of−0.25per regiment, to a maximum of−5at 20 regiments. This value scales linearly with the army maintenance slider.

Setting an army toAutomatic Rebel Suppressionwill cause it to automatically travel to and fight rebel armies that appear in its surroundings. It will not attack rebel armies it thinks it cannot beat. The army will return to its previous position after the rebels are dispatched. Armies that are ordered to move will stop suppressing rebels. An army cannot drill while doing this.

Units set to auto suppression reduce unrest by a greater amount than normal; to be exact, they suppress unrest at 500% effectiveness. But the cap of unrest reduction through rebel suppression still stays 5.

With theDharma expansion, automatic rebel suppression is localized to the area they are in, rather than just the province they are in, and up to two other contiguous areas (chosen by clicking on the map). The army then reduces unrest in all of those provinces via the "Friendly Troops" modifier, as though they were stationed in each individual province. This is more effective than simply stationing troops for a single area, but less effective (but usually still more efficient in manpower) across multiple areas.

#### Forced march[edit|edit source]

Forced march makes an army move 50% faster, but costs2military power[9]for each province the army marches through. Forced march is available atadministrative technology15. Armies that are forced marching do not recover morale. DuringAge of Revolutionsit is possible to enable the Improved Forced March Age ability, which reducesmilitary power cost to 0 (requiresMandate of Heaven). Additionally, completing both the Mercenary and Expansion idea groups will give you access to the Military policy "Hired Expeditions Act" which will also make Forced March cost no military power for as long as it is in effect.

### References[edit|edit source]

1. ↑See in/Europa Universalis IV/common/defines.lua: BASE_COMBAT_WIDTH = 15.0
1. ↑2.02.12.2FromDevelopment Diary 18th of January 2022:Regiments’ fire and shock pips now also count toward morale damage in their respective phases. Many of you will know that morale pips have been superior to fire and shock pips. This change will make the pips more equal in value, although morale pips may still be the better pick most of the time.
Regiments’ fire and shock pips now also count toward morale damage in their respective phases. Many of you will know that morale pips have been superior to fire and shock pips. This change will make the pips more equal in value, although morale pips may still be the better pick most of the time.

1. ↑FromDevelopment Diary 24th of May 2022:Reinforcement to backrow means something very different now vs in 1.32. In 1.32 it was a way to push further infantry/cavalry into the death pit that was the back row. Only after all inf/cav reserves were spent did artillery reinforce to the back, and once there they never left.Now (since 1.33) only cannons can be in the back row, and they can also retreat from it, which makes back row reinforcement an important (and positive) thing.From 1.34, each combat side will be limited to 2 back row reinforcements per day, plus 1 per 2 maneuver pips of the commanding general. This does not limit initial placement of artillery at battle start.
Reinforcement to backrow means something very different now vs in 1.32. In 1.32 it was a way to push further infantry/cavalry into the death pit that was the back row. Only after all inf/cav reserves were spent did artillery reinforce to the back, and once there they never left.

Now (since 1.33) only cannons can be in the back row, and they can also retreat from it, which makes back row reinforcement an important (and positive) thing.

From 1.34, each combat side will be limited to 2 back row reinforcements per day, plus 1 per 2 maneuver pips of the commanding general. This does not limit initial placement of artillery at battle start.

1. ↑FromDevelopment Diary 24th of May 2022:As mentioned above, EU4 has always had a bug (feature?) called Zombie Regiments.
In 1.34, regiments will always retreat and be replaced once either strength or morale reaches 0, removing the 12 day invincibility.
As mentioned above, EU4 has always had a bug (feature?) called Zombie Regiments.
In 1.34, regiments will always retreat and be replaced once either strength or morale reaches 0, removing the 12 day invincibility.

1. ↑http://steamcommunity.com/app/236850/discussions/0/864976115458051703/
1. ↑FromDevelopment Diary 24th of May 2022:Let me take this moment to briefly explain an existing feature: for each damage calculation, backrow artillery propagates half of the sum of relevant defensive pips to the regiment in front of them (rounding down). For example, the Leather Cannon will propagate 2/2=1 pip to strength damage calculation in the fire phase, and 1/2=0 pips during shock phase. For morale damage, it will propagate (2+1)/2=1 pip during the fire phase and (1+1)/2=1 pip during the shock phase.
Let me take this moment to briefly explain an existing feature: for each damage calculation, backrow artillery propagates half of the sum of relevant defensive pips to the regiment in front of them (rounding down). For example, the Leather Cannon will propagate 2/2=1 pip to strength damage calculation in the fire phase, and 1/2=0 pips during shock phase. For morale damage, it will propagate (2+1)/2=1 pip during the fire phase and (1+1)/2=1 pip during the shock phase.

1. ↑See in/Europa Universalis IV/common/defines.luaunderINF_LOOT,CAV_LOOTandART_LOOT.
1. ↑See in/Europa Universalis IV/common/static_modifiers/00_static_modifiers.txt(Static modifiers#Scorched Earth).
1. ↑This cost is affected by modifiers toall power costs and if the discount is at least−0.1%, the game rounds down the cost to1. The cost is specified as PS_FORCE_MARCH = 2 in/Europa Universalis IV/common/defines.lua.