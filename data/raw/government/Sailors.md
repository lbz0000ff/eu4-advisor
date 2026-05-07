Please help with verifying or updating older sections of this article.At least some were last verified forversion1.23.

Sailorsrepresent the trained seamen of a nation. Only coastal provinces provide sailors, and the amount of sailors depends on thedevelopmentof theprovince.

Sailors are used forshipsjust asmanpoweris used for troops. They differ from manpower both in what they are used for and in how they are acquired. Sailors are required when constructing new ships, and when ships are “repaired”. Not all ships require the same amount of sailors, with heavy ships needing the most and transports the least. A country whose stockpile of sailors is depleted will be unable to build new ships or repair damaged ones.

AI nations are coded to never run out of sailors since version 1.24 because they were too ineffective at managing them, so sailors are in effect only relevant to player nations.

### Contents

- 1Maximum
- 2Sailor increase
- 3Province sailors3.1Base3.2Sailor increase3.3Sailors efficiency3.3.1Local sailors modifier3.3.2National sailors modifier
- 3.1Base
- 3.2Sailor increase
- 3.3Sailors efficiency3.3.1Local sailors modifier3.3.2National sailors modifier
- 3.3.1Local sailors modifier
- 3.3.2National sailors modifier
- 4Using sailors4.1Sailor maintenance
- 4.1Sailor maintenance
- 5Sailors recovery5.1Sailor recovery speed
- 5.1Sailor recovery speed
- 6Mothball fleet
- 7Raid Coasts
- 8Exploit development
### Maximum[edit|edit source]

The maximum sailors available to a country is the sum of the province sailors.

### Sailor increase[edit|edit source]

EachGovernor General's Mansiontrade company investmentgives+400sailor increase.
And aninvasion nationhas asailor increase of+10 000men.[1]

### Province sailors[edit|edit source]

Province sailors is the amount of sailors each province contributes to the national sailor maximum. It is computed as follows:

#### Base[edit|edit source]

Base sailors is determined by thedevelopmentlevel of the province. Each level of development adds60men[2]. The starting development level of a province is a preset in the game files[3]. See theeconomic list of provincesfor these values. The development level of a province can be increased by spendingmonarch points.

#### Sailor increase[edit|edit source]

This local modifier is additional to base sailors.

#### Sailors efficiency[edit|edit source]

Sailors efficiency is the sum of all manpower modifiers of a province.

##### Local sailors modifier[edit|edit source]

- Dock
- Important Natural Harbor
- City
- Important Center of Trade
- Looted
##### National sailors modifier[edit|edit source]

- Maritime idea 2: Merchant Marine
- Venetian (upgraded) idea 5: Naval Conscription
- Venetian idea 5: Naval Conscription
- Dutch traditions
- Norwegian traditions
- Aragonese idea 2: Protection of the Coastlines
- Barbary Corsair idea 2: Galley Slaves
- Clanricarde idea 3: People of the Sea
- Navarran idea 5: People of the Sea
- Tunisian idea 4: Attract Foreign Pirates
- Maritime-Economic: The Recruitment Act
- Betsimisaraka traditions
- Manx traditions
- Bruneian idea 2: Sea Nomads
- East India idea 4: Presidency Armies
- Genoese idea 3: Rebuilding Genoese Trade
- Luccan idea 4: Luccan Naval Ambitions
- Alaskan idea 6: Alaskan Navy
- Lübeckian idea 3: Improved Shipbuilding
- Eora idea 4: Protect the Ancestral Land
- Iwi idea 1: Sons of Kupe
- Omani idea 3: Association With Unbelievers
### Using sailors[edit|edit source]

Sailors are used to man naval vessels and when raising marines. Different vessels require differing numbers of sailors to be at full strength. Similarly, sailors are required to return a damaged ship to full strength, and the number of sailors used to do this is an equivalent fraction of that for the whole ship (repairing a ship from 50% uses 50% of its initial sailor cost). It takes1000 sailors to recruit a Marine. Sailors are also used forreinforcingdepleted regiments.

#### Sailor maintenance[edit|edit source]

When fleets are on missions (i.e. not in port), they need 2% of the sailors build cost to maintain each month.

A number of ideas and bonuses can reduce the number of sailors needed for missions.

- Infrastructure-Maritime: Sailor Efficiency Act
- Estonian traditions
- Greek traditions
- Madyas traditions
- Sulawesi traditions
- Maritime idea 3: Sheltered Ports
- English idea 6: The Sick and Hurt Board
- Luzon idea 1: Barangay State
- Malayan Sultanate idea 5: Trading Fleets
- Siddi idea 2: Siddi Seamanship
- Swahili idea 1: Indian Ocean Trade
- Betsimisaraka ambition
- Hormuz ambition
- Moluccan ambition
- Arakanese idea 4: Magh and Ferenghi
- Kono idea 1: Shugo of Iyo
- Omani idea 5: End of the Shipbuilding Guilds
- So idea 6: Port Maintenance
### Sailors recovery[edit|edit source]

Sailors replenish over time until they reach the maximum level. It takes 10 years[5]to fill the sailor reserves from zero. The monthly recovery rate is:

If a nation owns at least one coastal province, sailors have a minimum recovery rate of5sailors per month.

#### Sailor recovery speed[edit|edit source]

Sailor recovery speed modifies the recovery rate of province sailors.

- Naval idea 5: Press Gangs
- English idea 6: The Sick and Hurt Board
- Piratical idea 7: Life of Liberty
- Estonian idea 2: Baltic Ties
- Hadramhi idea 5: Sailors of the Indian Ocean
### Mothball fleet[edit|edit source]

Mothballinga fleet will make it immobile and decrease its maintenance costs by 50%, and will cause it to lose 5% of the sailors in the fleet per month (also durability) until the fleet reaches a minimum of 25% sailors/durability. Sailors lost from mothballing are returned to the national sailor pool, but only up to the national sailor limit; any additional sailors above the limit are lost. Un-mothballing a fleet will cause it to repair at the standard rate.

### Raid Coasts[edit|edit source]

Certain nations can gain sailors fromraidinganother nation’s coastal provinces, even if the maximum number of sailors has been reached. A province that has been raided cannot be raided for another 10 years.

The efficiency of raiding is reduced by fleets onpirate hunting patrol.

### Exploit development[edit|edit source]

By exploiting thebase production of a province, a nation can get a large number of sailors instantly. Doing this will give 60 months worth of that province's sailors.

1. ↑See in/Europa Universalis IV/common/static_modifiers/00_static_modifiers.txt(Static modifiers#Invasion).
1. ↑See in/Europa Universalis IV/common/static_modifiers/00_static_modifiers.txt(Static modifiers#Development).
1. ↑See the files in/Europa Universalis IV/history/provinces.
1. ↑4.04.14.24.34.44.5See in/Europa Universalis IV/common/static_modifiers/00_static_modifiers.txt(Static modifiers).
1. ↑See in/Europa Universalis IV/common/defines.lua.