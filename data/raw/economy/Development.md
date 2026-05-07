Please help with verifying or updating older sections of this article.At least some were last verified forversion1.24.

Developmentis a province attribute, which replaces the former system of static basetaxandmanpower. There are three kinds of development in a province - base tax, production, and manpower, corresponding to administrative, diplomatic and military power respectively. Players can increase province development values (directly or subject owned) by usingmonarch power.

Province development is involved in someAgeObjectives:

- Having a cored province with at least 30 development is an objective in the Age of Discovery.
- Having a total development of at least 100 while the nation's capital isnotin Europe, Asia and Africa is another objective in the Age of Discovery.
- Having a capital with at least 50 development is an objective in the Age of Revolutions.
- Having a subject with at least 250 development is another objective in the Age of Revolutions.
### Contents

- 1Effects of development1.1Provincial level1.2National level
- 1.1Provincial level
- 1.2National level
- 2Developing a province2.1Development formula2.2Development cost2.2.1Development cost increase2.2.2Development cost modifiers2.2.3Development cost2.2.4Terrain-dependent local development cost2.2.5Climate-dependent local development cost2.2.6Ideas and traditions
- 2.1Development formula
- 2.2Development cost2.2.1Development cost increase2.2.2Development cost modifiers2.2.3Development cost2.2.4Terrain-dependent local development cost2.2.5Climate-dependent local development cost2.2.6Ideas and traditions
- 2.2.1Development cost increase
- 2.2.2Development cost modifiers
- 2.2.3Development cost
- 2.2.4Terrain-dependent local development cost
- 2.2.5Climate-dependent local development cost
- 2.2.6Ideas and traditions
- 3Exploiting development
- 4Settlement growth
- 5Concentrate development5.1Calculation
- 5.1Calculation
- 6AI behavior
- 7Strategy7.1Advanced tips
- 7.1Advanced tips
- 8References
### Effects of development[edit|edit source]

#### Provincial level[edit|edit source]

Aprovincegains per development level in:

Base tax:

+1yearly tax income base

Production:

Manpower:

+250maximummanpower

Irrespective of category, every point of development has the following effects on the individual province (note that only coastal provinces get sailor and naval force limit bonuses):

- +3%local development cost per point above 10 total development. This increase rises by 3% every 10 total development (+6%at 20,+9%at 30, etc.).
- +1%Province warscore cost
- +1%Provinceoverextensionvalue
- +10Corecreation cost
- +8Diplomatic annexation cost
- Increases the percentage of the local province culture in the player's nation.
- Increases the institution presence in the province by (new development level/6). This is capped at +10% increase.
- Most institution spread modifiers scale linearly with province development.
- Removes 5%devastation（with adjustment based on local autonomy).
Development levels over 30 no longer contribute to higher coring and culture conversion costs. For every 10 levels of development, a province gets an additionalbuildingslot.

#### National level[edit|edit source]

- A nation gains+1caravan powerfor each 3 total development, up to 50.
- A nation cannot bevassalizeddiplomatically if total development is more than 100 (−1000reasons).
- The base cost of annexation of a nation (before modifiers) is8 diplomatic power per development of the vassal nation.
- If the nation'sgovernmenttype allows for rank increases, having 300/1000 developmentis part of the requirement of becoming a kingdom/empirerespectively.
### Developing a province[edit|edit source]

Monarch points(,or) can be used to increase base tax, production, and manpower values, respectively. A province's base tax, production or manpower cannot be increased if its value is already more than that of the other two combined (for example, if the province's production and manpower are 1 each, then the base tax can not be raised above 3 and only an improvement of production or manpower is possible). In other words, the cap for one development type is equal to the sum of the other 2 plus 1.

Developing a province this way increases thecrownlandby0.2%per click.

#### Development formula[edit|edit source]

Development Cost Modifier: 0% by default, alters the base cost (50 before being modified). This modifier is uncapped.

Development Cost: 0% by default, impacts the cost to develop the province, capped at−90%.

Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{final cost} = 50 \cdot (1 + Development Cost Modifier + Local Development Cost Modifier) \cdot Max(0.1, 1 + Development Cost + Local Development Cost)}

Local development cost modifier andLocal development cost work exactly the same as their non-local counterparts, they exist purely as to distinguish global vs province-based modifiers.

The minimum cost of developing a province rounds down, with interesting implications describedbelow. The final cost can be 0, but it can not become negative even with more than−100%  Development Cost Modifier.

#### Development cost[edit|edit source]

##### Development cost increase[edit|edit source]

TheLocal Development Cost to develop provinces increases by +3% per point above 9 total development, +3% per point above 19 total development, and so on.

For example, a province upgrading from total development level 32 to 33 will have a totalLocal Development Cost of:

23 * 3% = 63% (23 levels above 9)

13 * 3% = 33% (13 levels above 19)

3 * 3% = 9% (3 levels above 29)

63% + 33% + 9% = 105%

This amount is added on top of the otherLocal Development Cost andDevelopment Cost.

##### Development cost modifiers[edit|edit source]

Must own less than 15/25/35/50 same continent provinces, depending on Age

Eranshahr(end-tag)

Also provides a 20% chance of increasingwhen manually increasing production in a province.

This table includes bothDevelopment Cost Modifier andLocal Development Cost Modifier as they're added together when calculating the cost of developing a province.

##### Development cost[edit|edit source]

Requires missionCombating the Diseasesavailable toInca,MayaorAztec

Aztec(mid-tag)

Persia(end-tag)Eranshahr(end-tag)

- PersiamissionLanguage of Poetrycomplete, in primary culture provinces
- EranshahrmissionAn Asha Empirecomplete, in primary culture provinces
Eranshahr(end-tag)

Only applies to owned coastal provinces with a Dock/DrydockandShipyard/Grand Shipyard when completing the mission.

If this mission is not completed asBohemiathen the modifier is permanent rather than tied to Bohemian national ideas.

This table includes bothDevelopment Cost andLocal Development Cost as they're added together when calculating the cost of developing a province.

##### Terrain-dependent local development cost[edit|edit source]

RequiresIncan"Among the Mountaintops" mission.

Can also be used by anyAndean Technology Group country even without the mission but the effects will be halved.

RequiresMayan"Adapting to the Environment" mission.

Can also be used by anyMayan faith orMaya culture country orMayawithout the mission but will only provide-10%

Available toMamluksorAjuuraanafter completing relevant missions.

Mamluks(mid-tag)

Requires eitherPlease the BurghersorLet the Ducat Roll(requirements)

Scandinavia(end-tag)

- Finland:"Integrate the Sami"
- Sweden:"Integrate the Sami"
- Scandinavia:"Let the Ducat Roll"(requirements)
Sweden(start-tag)

Scandinavia(end-tag)

Available toArabiaafter completing"The harsh desert" mission

##### Climate-dependent local development cost[edit|edit source]

##### Ideas and traditions[edit|edit source]

These modifiers lower the cost for developing a province.

- Alaskan idea 1: Aleutian Endurance
- Genevan idea 1: The Grand Council
- Great Armenian idea 2: Land Reclamation
- Tongan idea 3: The Islands of Maui
- Australian ambition
- Bukharan traditions
- Caspian traditions
- Colonial traditions
- Federation traditions
- Frisian traditions
- Garhwali traditions
- Goslar traditions
- Hojo traditions
- Rigan traditions
- Saxon traditions
- Tuscan traditions
- West Indies traditions
- Aboriginal idea 2: Fire-stick Farming
- Ajuuraan idea 5: Hydraulic Empire
- American Southwest idea 4: Prosperous Sedentarism
- Andean idea 5: Monumental Ornaments
- Ansbach idea 4: Protestant Exiles
- Armenian idea 2: Land Reclamation
- Asakura idea 3: Ichijodani City
- Assamese idea 2: Wet Rice Cultivation
- Ayutthayan idea 6: Phrai Luang
- Banteni idea 6: By the River
- Bengal Sultanate idea 3: Clear the Delta
- California Native idea 4: Forest Gardening
- Candarid idea 3: Ismail Bey Complex
- Cebu idea 7: Expand the Capital
- Chachapoyan idea 2: Legacy of Kuelap
- Charruan idea 1: Hunter-Gatherer Ways
- Colognian idea 3: Hanseatic Trade City
- Dali idea 6: Rice Terraces
- Date idea 7: Intensive Domain Development
- Dhundhari idea 4: Found the city of Jaipur
- Dithmarscher idea 5: Fortify the Coastline
- Dutch idea 3: Polders
- Eastern Algonquian idea 2: Seasonal Economy
- Egyptian idea 1: Centralization Works
- Farsi idea 7: A Capital for an Empire
- Finnish idea 4: Settle Middle Finland
- Flemish idea 2: Land Reclamation
- Garjati idea 4: Extend Tanks and Reservoirs
- Gelre idea 4: Rule the Rivers
- Golden Horde idea 6: Populating the Steppes
- Gutnish idea 1: Rebuild Visby
- Hanoverian idea 2: Weser Renaissance
- Hessian idea 4: Receive Religious Immigrants
- Hindustani idea 7: Proto-Industrialization
- Hormuz idea 6: Develop Qeshm and Hormuz
- Hosokawa idea 7: Horeki Reform
- Incan idea 2: Increased Obligations
- Israeli idea 6: People of Exile
- Isshiki idea 7: Expand our Ports
- Jaunpuri idea 4: Jaunpuri Architecture
- Kamilaroi idea 3: Fertile Soils of Kamilaroi
- Karamanid idea 5: Karamanid Architecture
- Kilwan idea 7: Center of Migration
- Kiwi idea 3: Piopiotahi
- Kuban idea 2: Children of Woot
- LPC idea 3: New Magdeburg Laws
- Lanfang idea 7: Expansion of the State
- Lithuanian (upgraded) idea 3: New Magdeburg Laws
- Luban idea 5: Lukasa Boards
- Luccan idea 3: Draining Lago di Bientina
- Madyas idea 3: Riches of the Visayas
- Mayan idea 2: Building Traditions
- Mewari idea 4: City of Lakes
- Milanese idea 3: Lowered Power of the Barons
- Mogadishan idea 4: City of Mogadishu
- Moravian idea 3: Cities of Moravia
- Mori idea 5: Hiroshima
- Nanbu idea 7: Defeating the Famines
- Neapolitan idea 3: Encourage City Living
- Nizhny Novgorod idea 2: Crossroads Of Nations
- Norse idea 4: Norse Artisans
- Pattani idea 7: Canal Infrastructure
- Pisan idea 4: Urbanization effort
- Plains Native idea 3: Bison Hunters
- Polotskian idea 7: Forest of Europe
- Rostov idea 1: Re-Unification of Rostov
- Satake idea 6: Strong Central Rule
- Semien idea 4: Builders and Artisans
- Siamese idea 4: Encourage Immigration
- Silesian idea 3: German Settlers
- Swiss idea 5: Oasis of Peace and Prosperity
- Texan idea 7: Adelsverein
- Venetian (upgraded) idea 7: Found the provveditori ai beni inculti
- Venetian idea 7: Found the provveditori ai beni inculti
- Zaporozhian idea 1: Fast Fort Builders
- Full Infrastructure
- Augsburger ambition
- Bavarian ambition
- Bolognese ambition
- French ambition
- Hausan ambition
- Kaurna ambition
- Lan Na ambition
- Mutapan ambition
- Pegu ambition
- Tokugawa ambition
- Tyrone ambition
- Administrative-Indigenous: Administration of Sacred Land
- Trading City traditions
- Aristocratic idea 2: Serfdom
- Divine idea 1: Servants of God
- Indigenous idea 1: Bountiful Land
- Plutocratic idea 6: Free Cities
- Bamberger idea 4: Little Venice
- Dalmatian idea 4: Center of Art and Literature
- Franconian idea 7: Franconian Bourgeoisie
- Great Moravian idea 4: Rebuild Veligrad
- Horn of African idea 3: Highland Cultivation
- Icelandic idea 6: Resilient Craftsmen
- Korean idea 4: Korean Artisanery
- Livonian idea 2: Border between East and West
- Lübeckian (Hansa) idea 5: Merchants with a State
- Persian idea 6: Promotion of Irrigation
- Prussian idea 7: Religious Toleration
- Sardinian-Piedmontese idea 5: Centralized State
- Vereenigde Oostindische Compagnie idea 3: Development of Foreign Lands
- Westphalian idea 2: Westphalian Decentralization
- Indigenous-Infrastructure: Indigenous Development Act
- Innovative-Indigenous: Disruptive Innovation
Some ideas and policies give development cost in primary culture provinces only:

- Navarran idea 7: An Industrious Folk
- Defensive-Economic: The Public Welfare Act
- Bohemian (upgraded) idea 7: Czech Nationalism
### Exploiting development[edit|edit source]

A province can be exploited for short-term benefits by permanently reducing its development by 1.

- ExploitBase Tax to gain 60 months worth of that province's tax income
- ExploitProduction to gain 60 months worth of that province's sailors
- ExploitBase Manpower to gain 60 months worth of that province's manpower
A province has to have at least 2 development in a category for it to be exploitable, and is required to have at least aterritorial core. A province cannot be exploited within the 20 years following its last exploitation, even if it changes owners.

### Settlement growth[edit|edit source]

It is also possible to develop provinces by promoting settlement growth in colonized provinces or cities. By placing the colonist on the little empty window to the top right of the province overview screen, the colonist will automatically start to improve the province. The development of that province will have a certain chance of increasing by 1 in a random category after each yearly tick in accordance to when you started to promote settlement growth. The chance of the colonist improving the base development is based on the amount of development in the province. This chance is also affected by Local Development Cost modifiers such as terrain, Universities, Expand Infrastructure, and local modifiers like those temporarily granted by events. The Settlement Growth mechanic is not affected by Global Settler Increase, New Settlers Chance, or any global development cost reductions.

The subject interaction "Block Settlement Growth" allows the overlord to prohibit a subject from using their colonist in this way, and instantly cancels any ongoing settlement growth.

### Concentrate development[edit|edit source]

Provinces in territories you own, or states controlled by a non-tributary subject, can be used to concentrate development in thecapital. This can be done on the state interface by selecting theconcentrate development button. Some of the development from provinces in the state is turned intomonarch power, which is then used to develop the capital. The tooltip over the concentrate development button shows the amount of monarch points, and the amount of development that will be gained (this usually displays higher than the actual result, explained below). Concentrate development will not be available if there is not enough development to produce enough monarch points to develop the capital.

Concentrating development in a subject will increase theirliberty desireby+3and decrease relations by−8per point of development taken.

#### Calculation[edit|edit source]

The amount ofbase tax ,production, orbase manpower removed from a province when concentrating isDevelopment category5{\textstyle {\frac {\text{Development category}}{5}}}rounded to the nearest whole number. For example a 3/2/2 province would become a 2/2/2 (−1/−0/−0) because only the first category rounds to at least 1. By the same logic, 13/7/4 would become 10/6/3 (−3/−1/−1). This also means if a state has no provinces with more than 2 development in any category, it cannot be used to concentrate development.

The amount of monarch points generated from development is equal to the development cost of the province. However the calculation is redone after each development category in the order tax → production → manpower. What this means is that an 8/8/8 province with a development cost of 80, will not get 6 x 80 total points but instead get 2 × 80 + 2 × 74 + 2 × 68 total points. As a resultadministrative will receive the most points, followed bydiplomatic, thenmilitary. This contradicts the in game tooltip, which implies that all categories use the initial value, as a result onlyadministrative is accurate.

Points generated from all provinces in a state are combined and then reduced by 20% (except for countries with Mandala System or Chakravarti government) and are then used to apply development to the capital. The initial development cost of the capital is what is used to applyallof the development, meaning there is no increase as points are applied.

The ideal use of this feature would be to somehow raise development cost in a territory or vassal state as high as possible, and decrease development cost in the capital as much as possible, this will gain the most monarch points from concentrating, and make the most use of points on the capital.

### AI behavior[edit|edit source]

AI generally will not develop provinces to more than original development × 2 or 10 development, whichever is higher. These numbers can be changed in defines.[1]

AI never exploit development, but may sometimes promote settlement growth.

The exception to this rule emerges when the AI develops one province for the purposes of institution spread, introduced inPatch 1.18, and also when developing coal provinces (even if the trade good isn't enabled yet) which can sometimes result in these provinces reaching over 40 development. At this time the exact behaviour of the AI regarding this is not well understood. The AI does not develop provinces anywhere as efficiently as a human player may do so.

### Strategy[edit|edit source]

- Prioritize provinces with 9 and 19 development (followed by 8 and 18, etc.) to open an additionalbuildingslot.
- Prioritize provinces from your own culture/culture group or culture convert before to gain the most from this development.
- Improve production in provinces with high value trade goods before provinces with lower valued goods.
- Evenly developing a province (4/4/4) is not as lucrative as weighting towards one type of development and reaping a greater bonus with an appropriate building (6/3/3 and achurch).
- Developing a coastal province instead of an inland province also improves sailors and trade power (through the+25%coastal province modifier).
- Consider timing: Is the province close to prosperity? Is an institution about to spawn? Is theUniversity about to finish construction? Is the parliamentary issue about to expire? Has the state edict reset time elapsed? Delaying or expediting development can save vital monarch points.
- Various missions and events  give an additional cost modifier (seelinked pageto “development cost”).
- Developing a province to get an institution can be expensive in terms of monarch points; it is recommended that the player choose to develop a province with multiple development costs that stack. To be specific, to attain the maximal reduction in development cost, the player should choose to locate their capital in a province with a level 2 or 3 Centre of Trade (the province has to be part of a state), temperate climate, farmlands, and that produces cloth or cotton. The following provinces have this combination of modifiers: Amsterdam, Baghdad, Cairo, London, Lublin, Macedonia, Milan, Prague, Regensburg, Warszawa and Wroclaw. These provinces have a cumulative reduction in developing cost of −20%/25% (−5% from farmlands, −5%/-10% from level 2/3 CoT, −10% from cloth or cotton).
##### Advanced tips[edit|edit source]

Development formula:Failed to parse (SVG (MathML can be enabled via browser plugin): Invalid response ("Math extension cannot connect to Restbase.") from server "https://en.wikipedia.org/api/rest_v1/":): {\displaystyle \text{final cost} = 50 \cdot Max(0.1, 1 + Development Cost Modifier + Local Development Cost Modifier) \cdot Max(0.1, 1 + Development Cost + Local Development Cost)}

Given that the development formula above rounds down we have some interesting implications whenDevelopment Cost is -90% or less:

At 0%Development Cost Modifier it will cost 5monarch points per point of development, meaning thatDevelopment Cost below -90% doesn't have any effect.

At -1%Development Cost Modifier it will cost 4monarch points per point of development, meaning that even a -2.5%Development Cost Modifier will be as impactful as a -20% (equivalent toadministrative techs level 17 and 23) on provinces with -90%Development Cost.

At -20%Development Cost Modifier it will cost 4monarch points per point of development, meaning thatDevelopment Cost Modifier is only useful in increments of 20% on provinces with -90%Development Cost, meaning that a -5%, -10% or -15%Development Cost Modifier by itself will have no effect on these provinces.

At -81%Development Cost Modifier it will cost 0monarch points per point of development, meaning that if it was somehow possible to stack enoughDevelopment Cost Modifier it would be possible to develop every province with -90%Development Cost for free until their development is high enough that they no longer get -90%Development Cost.

- Focus onDevelopment Cost Modifier for high development provinces whoseDevelopment Cost is so high that a small additive reduction won't be as effective.
- Since you get0.2%crownland per manual development most of the time, this means that at -90%it will cost just 125to get 5% more crownland or 1250 for 50% more crownland.
### References[edit|edit source]

1. ↑patch notes 1.15