Please help with verifying or updating older sections of this article.At least some were last verified forversion1.28.

Forts limit unit movement due to their zones of control ("ZoC"). This article explains precisely how theyused to work in version 1.28.

The key concept to understand is that movement of a unit depends on what its "Return Province" is, and not just on the province it is or the adjacent province it came from.

Note that all the information there has been worked out by experimentation and does not come from knowledge of the actual game code, and thus might potentially be inaccurate.

Many of the images in this article are in "Fort Level"map mode.

### Contents

- 1Concepts1.1ZoC and non-ZoC provinces1.2Return Province of a unit1.3Distance from Return Province1.4Previous Province of a unit1.5Merging and reorganizing units
- 1.1ZoC and non-ZoC provinces
- 1.2Return Province of a unit
- 1.3Distance from Return Province
- 1.4Previous Province of a unit
- 1.5Merging and reorganizing units
- 2Movement rules2.1Non-ZoC rule2.2Previous Province rule2.3Ship rule2.4Fort rule2.4.1Where the fort rule does NOT apply2.5ZoC rule2.5.1Where the ZoC rule does NOT apply
- 2.1Non-ZoC rule
- 2.2Previous Province rule
- 2.3Ship rule
- 2.4Fort rule2.4.1Where the fort rule does NOT apply
- 2.4.1Where the fort rule does NOT apply
- 2.5ZoC rule2.5.1Where the ZoC rule does NOT apply
- 2.5.1Where the ZoC rule does NOT apply
- 3Important consequences of the movement rules3.1A→C via B being allowed does not imply A→B→C being allowed3.2Pathfinding does not find the shortest path and depends on the Return Province
- 3.1A→C via B being allowed does not imply A→B→C being allowed
- 3.2Pathfinding does not find the shortest path and depends on the Return Province
- 4Other consequences of the movement rules4.1Clearing misconceptions4.2Miscellanous considerations4.3Combining units4.4Rings/barriers of ZoC provinces and defending with them4.5Attacking rings/barriers of ZoC provinces and getting trapped in them
- 4.1Clearing misconceptions
- 4.2Miscellanous considerations
- 4.3Combining units
- 4.4Rings/barriers of ZoC provinces and defending with them
- 4.5Attacking rings/barriers of ZoC provinces and getting trapped in them
- 5Reproducing the screenshots
- 6See also
### Concepts[edit|edit source]

#### ZoC and non-ZoC provinces[edit|edit source]

From the point of view of each country, the land provinces of the world are divided in ZoC provinces and non-ZoC provinces.

Let's consider you and an enemy at war. First, only forts that are non-mothballed and level 2 or higher project a ZoC; the enemy's capital with no fort buildings will not project a ZoC. Enemy forts will only project their zone of control (ZoC) onto enemy-ownedprovinces that are next to the fort province. There's one exception to the "enemy-owned" part: forts ofyoursthat an enemy captures in warwillextend the enemy's ZoC on not just enemy-owned provinces butalsoprovinces that you own. Enemy-nativeforts (forts on provinces the enemy alreadyowns, not just occupied in war -- e.g., forts in enemy provinces directly on your border) willnotproject their ZoC into provinces you already own. Then, if a province under the enemy fort's ZoC becomesoccupiedby you (but notownedby you, which can only happen via later annexation), this willnotexclude it from the enemy fort's ZoC. If you siege the enemy fort and occupy its province, it will no longer project a ZoC for the enemy, but it will now project one foryouthat blocks theenemy'stroop movements since it now acts like your fort! Further, in reflecting the exception from before, thiscapturedfort will also project its ZoC over enemy-owned provinces while your native forts (forts in provinces you already own) will not project a ZoC over enemy-owned provinces.

Occupation by anyone of a province without a fort will never change ZoC because occupation status only matters for the fort itself. The only way to maintain the occupation status for the attacker is to maintain at all times a unit on said province; otherwise, the occupied status will be removed about a month after the last attacking unit left the province. Another way to do that is to besiege the fort that created the zone of control over the province, for as long as the siege will last no province within its zone of control will be able to be liberated.

ZoC provinces have a tooltip that says "Within the FORT COUNTRY fort in FORT PROVINCE's zone of control", and have bars in the Fort map mode.

It doesn't apparently matter which fort a province is in the ZoC of and thus multiple forts don't introduce complications. Incidentally, the game apparently assigns ZoC using a single global ordering of forts, and a fort can thus be in the ZoC of another fort rather than itself, although this seems to have no effect, as a fort exercises its zone of control prioritarily on the province it is built. As a rule, when a fort is occupied, it can only be liberated after a regular army sieged it down again (or if the war ended). So, even if a fort lies in the ZoC of one or several allied forts, its owner will still have to send an army to besiege it again in order to get it liberated.

ZoC only applies to issuing movement orders, it does not apply to any movement orders issued before the ZoC existed. For example, if a fort is mothballed and then activated after an army is queued to walk past it the army will walk past unmolested.

- The mothballed fort at Selanik doesn't prevent movement to Filibe
The mothballed fort at Selanik doesn't prevent movement to Filibe

- One day after the fort at Selanik is unmothballed, it immediately prevents new movement commands to Filibe, even with 0 garrison
One day after the fort at Selanik is unmothballed, it immediately prevents new movement commands to Filibe, even with 0 garrison

- The fort in Ankara projects ZoC in the neutral province of Kastamonu, preventing movement from Canik to Bolu
The fort in Ankara projects ZoC in the neutral province of Kastamonu, preventing movement from Canik to Bolu

- In 1792 the province of Nice is a ZoC province from the point of view of Sardinia-Piedmont due to the fort of Cuneo (Coni) being occupied...
In 1792 the province of Nice is a ZoC province from the point of view of Sardinia-Piedmont due to the fort of Cuneo (Coni) being occupied...

- ...even though Nice is an unoccupied province that we own!
...even though Nice is an unoccupied province that we own!

#### Return Province of a unit[edit|edit source]

Each land unit stores a "Return Province", which is the last non-ZoC land province or sea tile it left (in the "previous_war" variable in the save file), if it hasn't been reset due to becoming ZoC since.

The Return Province is updated when a unit leaves a non-ZoC province, not when it enters it! This matters, as describedbelow. The Return Province is also cleared if it becomes a ZoC province, which means the Return Province is guaranteed to always be a non-ZoC province (or a sea tile). It seems that nothing else other than these two events affects the Return Province, including for instance sieging down a fort such that your unit is now in a non-ZoC province.

Note that the Return Province won't be reset if it becomes militarily inaccessible, and in fact that has no effect on movement as described in the ZoC rule (you can even move to the Return Province itself if it's inaccessible!).

When a player-controlled unit is in a ZoC province, the Return Province is shown on the map as a green flag, with the tooltip saying "Return province". Note that if you are in a non-ZoC province, there will still be a Return Province that will be used for the first movement command away from it (since it's only updated when you leave a non-ZoC province), but it won't be shown with a green flag on the map.

For non-player-controlled units and player controlled units in a ZoC province, there doesn't seem to be a way to determine what their Return Province is, other than watching their movements and remembering it, or saving the game and looking at the save file in a text editor.

The allowed movement of a unit depends not only on the province it is in, but also on its Return Province (and the Previous Province, although it only rarely matters).

- Return Province indicator. Only shown for friendly units in a ZoC province, but all units have a Return Province stored.
Return Province indicator. Only shown for friendly units in a ZoC province, but all units have a Return Province stored.

#### Distance from Return Province[edit|edit source]

Each province can be thought to have a distance from the Return Province corresponding to the number of provinces in the shortest among the paths starting from it and visiting non-ZoC land provinces you have military access to, regardless of blocked straits, and then ending with either a non-ZoC province, a ZoC province or a ZoC province without a fort controlled by an enemy followed by a ZoC province with a fort controlled by an enemy (if there are no such paths, assign an infinite distance).

It seems that the movement rules only care about whether provinces are at distance 0, 1 or 2 from the Return Province, as the ZoC rule allows you to move to them if they don't have a non-neutral fort, and that the distance from the Return Province is otherwise irrelevant.

- Distances from Return Province Vidin
Distances from Return Province Vidin

- Distances from Return Province Nigbolu
Distances from Return Province Nigbolu

#### Previous Province of a unit[edit|edit source]

Each unit stores the Previous Province, i.e. the adjacent province it came from (in the "previous" variable in the save file). There doesn't seem to be a way to tell what it is from the game UI.

There's a movement rule that lets you go back to the Previous Province, but in most cases the Previous Province is already accessible according to the other rules.

Exceptions are due to the movement patterns made possible by the Return Province being only set when leaving a province, or due to the land or diplomatic landscape somehow changing.

Note that only the immediately previous province is stored, so you can't go back arbitrarily far.

#### Merging and reorganizing units[edit|edit source]

If you merge units, the merged unit has the Return Province of one of the merged units; it seems that it is the Return Province shown on the map when the multiple units are selected, which seems to be the one of the first unit in the list from which the merged unit also takes its name from; in turn, the list seems to be ordered according to the creation date of the army (where merging doesn't count as creation).

However, if you use the Reorganize Units button instead of the Merge button, and the units don't both have a general in hostile territory, it is possible to move all regiments from a unit into another, and the Return Province of the unit you moved regiments to is of course used for the resulting unit.

Seebelowfor a detailed instructions on how to combine units with the desired Return Province in almost all cases.

### Movement rules[edit|edit source]

Movement to a non-adjacent province is possible if and only if movement is possible "step by step" but without updating the Return Province between each step (this sometimes matters as described below). Note that the Return Province is updated after each non-ZoC province is left even if a non-adjacent movement command is sent and the lack of update only matters when deciding if the movement is allowed. Battles do not cancel movement commands, and movement resumes once the battle ends (assuming the unit did not retreat or got stack wiped).

Note that all ZoC rules are checked at the time the movement order is given. Changes in ZoC afterwards are ignored.

Movement to an adjacent province is only possible if you have military access to it (with the exception of moving to the Return Province) and if there isn't a blocked strait (with no exceptions). For rules about when a strait is blocked, seeNaval warfare § Blocking a strait.

Once that is satisfied, then movement is possible if any of the following rules applies.

#### Non-ZoC rule[edit|edit source]

You can always move from a non-ZoC province to any adjacent province.

#### Previous Province rule[edit|edit source]

You can always move back to the Previous Province, i.e. the adjacent province you came from.

- Moving from Tirgoviste to Silistre is only possible due to the Previous Province rule since the Return Province is in Constantinople.
Moving from Tirgoviste to Silistre is only possible due to the Previous Province rule since the Return Province is in Constantinople.

#### Ship rule[edit|edit source]

You can always move to a transport ship in an adjacent sea tile.

- Moving to the ship in the Aegean Sea is only possible due to the Ship rule since the Return Province is in Nigbolu.
Moving to the ship in the Aegean Sea is only possible due to the Ship rule since the Return Province is in Nigbolu.

#### Fort rule[edit|edit source]

Moving to any non-neutral fort is possible if

- you arenoton a fort controlled by an enemy,or
- the target fort is directly adjacent to the Return Province or is the Return Province.
- Can move from Silistre to the fort in Tirgoviste even though the Return Province is at Constantinople and separate by ZoC provinces Edirne and Kirkkilise
Can move from Silistre to the fort in Tirgoviste even though the Return Province is at Constantinople and separate by ZoC provinces Edirne and Kirkkilise

- Moving to Constantinople is only possible due to the Fort rule since the Return Province is in Nigbolu (and you can't just move to non-ZoC provinces behind ZoC)
Moving to Constantinople is only possible due to the Fort rule since the Return Province is in Nigbolu (and you can't just move to non-ZoC provinces behind ZoC)

- Can move from the fort in Barrois to the fort in Rethel because the fort in Rethel is adjacent to Return Province Lützelburg.
Can move from the fort in Barrois to the fort in Rethel because the fort in Rethel is adjacent to Return Province Lützelburg.

- Can move from the fort in Avignon to the fort in Provence because the latter is adjacent to Return Province Cote d'Azur.
Can move from the fort in Avignon to the fort in Provence because the latter is adjacent to Return Province Cote d'Azur.

##### Where the fort rule does NOT apply[edit|edit source]

- Can no longer move to Constantinople after deleting the fort there and moving the capital away, since the Return Province is in Nigbolu and you can't just move to non-ZoC provinces behind ZoC.
Can no longer move to Constantinople after deleting the fort there and moving the capital away, since the Return Province is in Nigbolu and you can't just move to non-ZoC provinces behind ZoC.

- Cannot directly move from the fort in Edirne to the fort in Selanik because the latter is not adjacent to Return Province Nigbolu.
Cannot directly move from the fort in Edirne to the fort in Selanik because the latter is not adjacent to Return Province Nigbolu.

- Cannot directly move from the fort in Avignon to the fort in Provence because the latter is not adjacent to Return Province Ligurian Sea.
Cannot directly move from the fort in Avignon to the fort in Provence because the latter is not adjacent to Return Province Ligurian Sea.

- Cannot directly move from Üsküp to the capital fort in Lezhë using the fort rule because it is not a non-neutral fort
Cannot directly move from Üsküp to the capital fort in Lezhë using the fort rule because it is not a non-neutral fort

#### ZoC rule[edit|edit source]

From a ZoC province you can always directly move to any province without a non-neutral fort that is one of

- the Return Province
- adjacent to the Return Province
- adjacent to a militarily accessible non-ZoC province that is adjacent to the Return Province
i.e. any province with distance from the Previous Province as previously defined up to 2.

It doesn't matter whether there is a blocked strait in the path from the Return Province to the target province (but of course they matter in the movement itself).

It doesn't matter whether you have military access or not to the Return Province, and you can even move to it if you don't have military access to it (but you need access to the target province and the intermediate one in the path, if any).

- Movement between Filibe and Sofya is possible because Sofya is adjacent to Return Province Nigbolu.
Movement between Filibe and Sofya is possible because Sofya is adjacent to Return Province Nigbolu.

- Movement between Sofya and Üsküp (with access to Serbia) is possible because Üsküp is at distance 2 from Return Province Vidin (through Nis).
Movement between Sofya and Üsküp (with access to Serbia) is possible because Üsküp is at distance 2 from Return Province Vidin (through Nis).

- It's still possible to move back to Return Province Kosovo even after revoking military access to Serbia and thus not having military access there.
It's still possible to move back to Return Province Kosovo even after revoking military access to Serbia and thus not having military access there.

- It's possible to move all along the coast from Mentesha to Morea, because all those provinces are adjacent to Return Province Aegean Sea, and the forts in the path are adjacent to Return Province Aegean Sea (the Fort rule applies when moving into the forts)
It's possible to move all along the coast from Mentesha to Morea, because all those provinces are adjacent to Return Province Aegean Sea, and the forts in the path are adjacent to Return Province Aegean Sea (the Fort rule applies when moving into the forts)

- It's possible to move to Bikol from Manila because it is at distance 2 from Return Province Panay via Visayas, even though there are two blocked straits in the way
It's possible to move to Bikol from Manila because it is at distance 2 from Return Province Panay via Visayas, even though there are two blocked straits in the way

##### Where the ZoC rule does NOT apply[edit|edit source]

- Movement between Sofya and Üsküp (without access to Serbia) is impossible because there is no path from Return Province Nigbolu to Üsküp that doesn't pass through a ZoC province or an inaccessible province
Movement between Sofya and Üsküp (without access to Serbia) is impossible because there is no path from Return Province Nigbolu to Üsküp that doesn't pass through a ZoC province or an inaccessible province

- Movement between Sofya and Üsküp with access to Serbia is only possible indirectly because Üsküp is at distance 3 from Return Province Nigbolu (through Vidin and Nis).
Movement between Sofya and Üsküp with access to Serbia is only possible indirectly because Üsküp is at distance 3 from Return Province Nigbolu (through Vidin and Nis).

- Movement between Üsküp and Kesriye with access to Serbia (but without access to Albania) is impossible because there is no path from Return Province Vidin to Kesriye that doesn't pass through a ZoC province.
Movement between Üsküp and Kesriye with access to Serbia (but without access to Albania) is impossible because there is no path from Return Province Vidin to Kesriye that doesn't pass through a ZoC province.

- Movement between Üsküp and Kesriye with access to Serbia and Albania is only possible indirectly because Kesriye is at distance 5 from Return Province Vidin (through Nis, Kosovo, Lezhë and Avlonya). It's also impossible to move directly to Lezhë rather than via Kosovo because it's at distance 3 and it's not a non-neutral fort.
Movement between Üsküp and Kesriye with access to Serbia and Albania is only possible indirectly because Kesriye is at distance 5 from Return Province Vidin (through Nis, Kosovo, Lezhë and Avlonya). It's also impossible to move directly to Lezhë rather than via Kosovo because it's at distance 3 and it's not a non-neutral fort.

- When the Return Province is Gulf of Satalia instead of Aegean Sea, it is no longer possible to move from Mentesha all along to Morea, but only to Aydyn, since the provinces are not reachable without passing through ZoC provinces.
When the Return Province is Gulf of Satalia instead of Aegean Sea, it is no longer possible to move from Mentesha all along to Morea, but only to Aydyn, since the provinces are not reachable without passing through ZoC provinces.

- After having given Bosnia ownership of Zeta via a peace deal, getting access to Serbia and moving to Üsküp from Return Province Vidin, revoking access to Serbia, getting access from Hungary, Albania and Bosnia, it's not possible to move from Üsküp to Lezhë, because even though the distance to Lezhë from Return Province Nigbolu is now lower than the distance from Üsküp (by passing through Hungary), that distance is greater than 2.
After having given Bosnia ownership of Zeta via a peace deal, getting access to Serbia and moving to Üsküp from Return Province Vidin, revoking access to Serbia, getting access from Hungary, Albania and Bosnia, it's not possible to move from Üsküp to Lezhë, because even though the distance to Lezhë from Return Province Nigbolu is now lower than the distance from Üsküp (by passing through Hungary), that distance is greater than 2.

### Important consequences of the movement rules[edit|edit source]

Note that these are almost certainly unintended, and so the rules may hopefully be changed in a future patch to remove these dubious properties of the current system.

#### A→C via B being allowed does not imply A→B→C being allowed[edit|edit source]

Unfortunately, in the current ruleset, it is sometimes possible that, with A being a non-ZoC province, you can move from A to C with a single movement command resulting in a path passing through B, but that you can't move from A to C with two movement command from A→B and B→C.

The reason for this is that the Return Province is only updated when leaving a non-ZoC province (and not when entering it), but indirect movement commands are computed without updating the Return Province. This means that whether B→C is allowed will be evaluated with Return Province A if you first move to B (because you left it), but will be evaluated with whatever Return Province the unit had as it reached A if you directly move to C.

This can result in suprising behavior and being trapped beyond sieged forts if you move your sieging units incorrectly, as described later.

- The 4k stack can move to Silistre via land because it has just come off the ship and thus has Return Province Gulf of Varna, which is adjacent to Silistre. The other two units instead left Constantinople after unloading from the ship and thus have Return Province Constantinople, and cannot move to Silistre via land
The 4k stack can move to Silistre via land because it has just come off the ship and thus has Return Province Gulf of Varna, which is adjacent to Silistre. The other two units instead left Constantinople after unloading from the ship and thus have Return Province Constantinople, and cannot move to Silistre via land

- After sieging down the fort in Severia, the 6k unit was moved to Czerkasy with a single command, which was allowed based on Return Province Czerkasy, while the 13k unit was first moved to Perayaslav and is now trapped in the enemy territory because its Return Province is now set to Severia. It needs to be rescued using Reorganize Units as described in the part of the article that deals with being trapped after sieging.
After sieging down the fort in Severia, the 6k unit was moved to Czerkasy with a single command, which was allowed based on Return Province Czerkasy, while the 13k unit was first moved to Perayaslav and is now trapped in the enemy territory because its Return Province is now set to Severia. It needs to be rescued using Reorganize Units as described in the part of the article that deals with being trapped after sieging.

#### Pathfinding does not find the shortest path and depends on the Return Province[edit|edit source]

Pathfinding does not update the Return Province when pathfinding, which means that it will not consider all paths that can be performed step by step, and for example will never choose a path that moves between two ZoC provinces without forts that are far away, even though such a path might be possible if performed step by step.

Thus, pathfinding can depend on where the unit comes from, even when in a non-ZoC province, as shown in the following example.

- Two units in Branicevo find different paths to Üsküp! This is because one has its Return Province set to Torontal and the other has it set to Nis (since they came from those provinces). The one with Return Province set to Torontal can't consider moving from Sofya to Üsküp because Üsküp is at distance 3 from Torontal.
Two units in Branicevo find different paths to Üsküp! This is because one has its Return Province set to Torontal and the other has it set to Nis (since they came from those provinces). The one with Return Province set to Torontal can't consider moving from Sofya to Üsküp because Üsküp is at distance 3 from Torontal.

### Other consequences of the movement rules[edit|edit source]

#### Clearing misconceptions[edit|edit source]

- It is not true that you can always move from a ZoC to a non-ZoC province.
- It is not true that you can never move from a province next to a fort to another province next to a fort.
- It is not true that you can never move between enemy forts. You can do so if both are adjacent to the Return Province.
- You cannot move beyond ZoC even to your own territory, unless you have a fort (including just a capital fort) there and you are moving from a province without an enemy fort
- Recently unmothballed forts with 0 garrison still project ZoC (but they can be sieged in one tick like an unfortified province)
#### Miscellanous considerations[edit|edit source]

- Movement, except for movement on provinces containing a fort, only depends on whether a province is within the ZoC of a fort, but it doesn't depend on the actual position of the forts or whether fort ZoCs overlap or not
- Building new forts never makes more provinces accessible to the enemy, except possibly for the new fort province itself, if it is next to an enemy-reachable ZoC province without a fort
- A "ring" of ZoC provinces will make any contained province inaccessible (even if it's non-ZoC) unless it's a fort adjacent to a province of the outer border that doesn't contain a fort
- It's best to move into ZoC territory from a non-ZoC province that is equally distant to many ZoC provinces as opposed to moving from a province that is "off to a side", so that you can move more directly in the ZoC territory
- It may be best to do an amphibious landing into a ZoC province as opposed to into a non-ZoC province if the sea tile is adjacent to many ZoC provinces as you can then freely move between the ZoC provinces on the coast since your Return Province remains set to the sea tile
#### Combining units[edit|edit source]

As described in the rules, if when selecting multiple units the desired Return Province is shown, you can just use the Merge button to combine them.

Otherwise, if you have more than two armies to combine, first merge all the armies other than the one with the desired Return Province.

Then, unless both units have general and are in hostile territory, you can use the Reorganize Units button instead of the Merge Button to move all regiments into the unit whose Return Province you want to use.

If both units have a general and you are in hostile territory, then you can create a new unit with one regiment from any unit with at least 2 regiments and then use Reorganize Units to move all the regiments (and general) from the unit with the undesired Return Province to the newly created unit. Now that newly created unit should be last in the list, and thus merging should result in the desired Return Province.

In case you have exactly two armies with exactly one regiment each and both with leaders in hostile territory, there doesn't seem to be any way to combine the units with the Return Province being set to the Return Province of the second unit in the list other than editing the save file by swapping the "previous_war" values of the two armies, loading it and merging them.

#### Rings/barriers of ZoC provinces and defending with them[edit|edit source]

In general a "ring"/"barrier" of ZoC provinces (somewhat more formally, consider, for each connected component of ZoC provinces, the ones that are reachable from any province far away passing only by non-ZoC provinces) will prevent passage from outside to inside and from inside to outside, with the exception of fort directly adjacent to a ZoC province of the ring that doesn't itself contain a fort.

This means that if all the provinces on the border of your country are in the ZoC of a fort, regardless of the exact fort layout, it will be impossible to reach the inside of your country without sieging forts first, no matter where the enemy comes from or how it moves.

This can be used to make sure your standing army cannot be immediately wiped out and give you time to use those unreachable interior provinces to train mercenaries non-stop until your overall army is bigger and then relieve the siege with guaranteed defender bonuses in combat (this means it's best to place forts in defensive terrain). Without such a fort setup, an enemy with a superior army could instead invade, immediately reach and wipe out your army, and then carpet siege all provinces to guarantee a 100% warscore victory.

Of course forts have expensive maintenance, so this strategy is only optimal if you expect an alliance of enemies with an army superior to yours to declare a surprise war, and if the forts would be less expensive that simply getting a large enough standing army, possibly involving paying for being over the force limit and/or paying for standing mercenaries.

If you don't form such a ring of ZoC provinces (as well as natural barriers like other countries that won't give military access to the enemy and that are fortified themselves, or the sea if you are sure you will have naval superiority), forts will not make any part of your country inaccessible. However, they can still slow down the enemy and possibly cause him to split its forces, as well as preventing the ZoC provinces from being asked for in a peace deal if the fort has not been sieged.

#### Attacking rings/barriers of ZoC provinces and getting trapped in them[edit|edit source]

When you are the attacker, you run the risk of getting trapped behind rings or barriers of ZoC provinces if you don't move your units very carefully.

In particular, if you siege down a inner redundant fort without other nearby forts, such that there is still a ring of ZoC provinces enclosing an interior region after sieging the fort and that the fort you sieged is now in that interior, you run the risk of being trapped.

If after such a siege you move either to an inside non-ZoC province, or to a province on the ring of ZoC provinces, your Return Province will be reset to the fort, which means that you are now "considered inside" the ring and won't be able to get out normally.

If however you directly, with a SINGLE movement command, move to the outside by right clicking on an outside non-ZoC province, you will be able to get there, because sieging down a fort does not reset the Return Province, which will still be on the outside.

If you make a mistake and get your units trapped, you can still usually move them to a ZoC province on the ring and have them meet up with a unit coming from the outside (such as a single mercenary infantry regiment; note that you must build it in an outside non-ZoC province and move it to the ZoC province, not build it directly in an occupied ZoC province on the ring, as it then won't be able to move at all except to a nearby fort or ship!). You can then follow the advice inCombining unitson how to use the Reorganize Units feature to combine these two units in a way that results in a unit that can move back outside where your "liberating unit" came from.

In addition to that, if both a unit of yours and its Return Province is next to an enemy fort you occupied and the enemy sieges it back, the Return Province will be reset as it becomes ZoC again and your unit will be in a ZoC province, meaning that the ZoC rule will not apply and you will only be able to move the unit to a nearby enemy fort, to a transport ship or to the Previous Province, unless you rescue it by combining units (if the province is still reachable by any of your other units).

Thus, if you need to park a unit in such a position, it may be smart to make sure you moved it to the province from a province that won't become ZoC as a result of the enemy resieging forts, so that you can go back there.

### Reproducing the screenshots[edit|edit source]

To reproduce the screenshots, start in normal mode and use the "god", "yesman", "winwars" and "fast_diplo" and "ai" console commands. Make sure that enemy forts are not mothballed unless you want to test how they behave when mothballed. To siege forts more quickly, use "leader 99 99 99 99" to get a 99 siege general. Use the "tag" command to switch to other countries and then the "ai" command to again disable the AI of the country you switched from.

The screenshots are produced by starting and declaring war in one of these ways:

- Byzantium vs Ottomans in 1444
- Austria vs France in 1792
- Commonwealth vs Russia in 1792. You need to tag switch to Russia, make peace and delete the fort in Kursk and build one in Severia.
- Maguindanao vs Spain in 1792. You need to tag switch to Spain and build a fort in Tondo and some ships in nearby provinces to block the straits.
### See also[edit|edit source]

- Video guide byReman's Paradox:Guide to Fort Zone of Control Mechanics