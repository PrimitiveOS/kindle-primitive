# PrimitiveOS gameplay references

This review covers the seven games in the current lineup. The games use original Kindle interfaces, artwork, and levels. The sources below describe the rules and controls used to check each game. Desktop tests exercise gameplay and inputs. Physical e-ink timing remains unverified.

## 2048

Cirulli's original starts with two tiles on a 4 × 4 board. A move slides every tile in the chosen direction. Two equal tiles merge once per move and add their combined value to the score. A changed board gains a 2 or a 4 in a random empty cell, with a 90% chance of a 2. Reaching 2048 offers the player the option to keep going. The game ends when no legal moves remain. [Original game](https://gabrielecirulli.github.io/2048/) · [Original game rules in source](https://raw.githubusercontent.com/gabrielecirulli/2048/master/js/game_manager.js)

The Kindle version uses whole-board swipes and direction buttons, with score and best score visible throughout. The 2048 tile behaves like any other merge and play continues immediately. A regression test covers a score in the millions and a merge beyond 2048. The original Kindle line puzzles retain their own saves under **Line puzzles**.

## Snake

The Nokia 6110 manual describes continuous movement, eating to grow, a saved top score, selectable difficulty, pause and resume, and collisions with the wall or the snake's own tail. Nokia's retrospective describes level-weighted scoring across nine levels, plus 100 points for completing the board. The later 3310's Snake II also supports wraparound, bonus food, and mazes. [Nokia 6110 manual, pages 50–52](https://altehandys.de/downloads/man-no-6110.pdf#page=51) · [Nokia Snake history](https://blogs.windows.com/devices/2009/01/20/history-of-nokia-part-2-snake/) · [Nokia 3310 retrospective](https://blogs.windows.com/devices/2009/04/27/nokia-3310/)

The 6110 rules are the reference for Kindle. Pick a speed from 1 to 9 before a round. The snake moves at that pace until it hits a wall or its own body, and each bite earns points at the chosen speed. Filling the board adds 100 points. Each step takes 850 to 450 ms, depending on the speed setting. The board uses an original 16 × 16 layout, onscreen arrows and swipes. The renderer schedules individual steps to limit e-ink redraws.

## Starship

Bandai Namco's Galaga Wars+ documents touch steering, automatic fire, waves and bosses. Infinite Dreams' Sky Force Reloaded uses scrolling missions and bosses. Together they establish the mobile shooter loop of moving to dodge fire and line up shots while enemies keep moving. [Galaga Wars+ developer listing](https://apps.apple.com/us/app/galaga-wars/id1574668118) · [Sky Force Reloaded developer listing](https://apps.apple.com/us/app/sky-force-reloaded/id976116090)

Starship now uses tap and swipe steering, automatic fire, traveling shots, three standard waves, and a fourth wave against an original flagship. A stationary background and 420 ms simulation steps limit refreshes on e-ink. An automated pilot test clears the entire mission, including the flagship, without taking damage. Any earlier turn-based save remains in a separate file.

## Nonogram

In a black-and-white nonogram, each clue gives the length of a filled run. The clues follow the order of the runs in each row and column. Adjacent runs have at least one empty square between them. Conceptis documents these rules and offers a mobile version with drawing and clue helpers. [Conceptis rules](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/pic-a-pix/rules) · [Conceptis mobile edition](https://apps.apple.com/us/app/nonogram-b-w-pic-a-pix/id6746461692)

The Kindle game offers fill and X marks, clue completion, and saved boards. Empty squares may be left unmarked. Tests confirm that each of the twelve original pictures has exactly one solution.

## Crate Shift

The original box-pushing rules allow a worker to push a single box into a free square. Boxes cannot be pulled or pushed in groups. The puzzle is solved when every box reaches a marked destination. Thinking Rabbit's mobile edition also uses touch gestures. **Crate Shift** is the title for our original levels and artwork. [Official Sokoban rules and branding](https://www.sokoban.jp/rule.html) · [Sokoban Touch developer listing](https://play.google.com/store/apps/details?hl=en&id=jp.thinkingrabbit.sokobantouch_free)

Crate Shift moves one square per swipe or tap. It tracks moves and preserves undo history. Walls and other crates block pushes. Tests cover blocked double pushes, all eight solutions, and the target marker under the worker.

## Memory Match

Ravensburger's rules describe shuffling the cards face down, revealing two cards per turn, and leaving a mismatched pair face up briefly before returning it to the same positions. The mobile edition includes solo play. Nokia's Memory also measures how few tries it takes to find every pair and keeps matches visible. [Ravensburger rules](https://www.ravensburger.org/spielanleitungen/ecm/Spielanleitungen/26632%20anl%201429398.pdf) · [Ravensburger mobile edition](https://play.google.com/store/apps/details?hl=en&id=com.ravensburger.memory) · [Nokia 6110 manual, page 51](https://altehandys.de/downloads/man-no-6110.pdf#page=51)

The Kindle version follows the solo rules. A turn consists of two taps, found pairs stay visible, and a mismatched pair closes after one second. A test verifies that a third card stays closed while the mismatch is visible.

## Switchyard

Mobile railway games use different rules. Railbound asks players to lay track and couple carriages to a locomotive. Train Switch uses pre-laid tracks and taps to move junctions while trains are approaching. These games share the idea of routing a train to the right destination. [Railbound developer listing](https://play.google.com/store/apps/details?id=com.Afterburn.Railbound) · [Train Switch developer listing](https://play.google.com/store/apps/details?id=com.barmanstudio.traingame)

Switchyard keeps its original one-train puzzle. The player sets points on existing tracks and dispatches the train, then sees the route it took to the depot or buffer. Each of its eight original yards has a tested solution.
