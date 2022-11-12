# Upside Down Tetris

Forked from: [CelestialAmber/TetrisNESDisasm](https://github.com/CelestialAmber/TetrisNESDisasm)

This is me learning how to computer a little bit better by seeing if I could make tetris play up instead of down.

This is what has been done:

- Pieces spawn at the bottom
- The pieces go up instead of down
- The Z & S pieces have been shifted up by one value in the orientation table
- T L, J & T pieces' orders have been swapped in the orientation table so that the spawning piece is the one that points up.  The order of each turn has been preserved.
- The orientation table's individual pieces have been rearranged so that the 4th tile described is at the highest point (This may not have been necessary)
- The code that checks 4 lines for clears starts from the bottom and works up, as clears are found, the board below is shifted up by one
- Row 0 has been hacked to show a line clear animation when applicable.
- The curtain is drawn up instead of down
- The T, L & J pieces' depictions in the next box have been altered to point up
- The same with the statistics table
- The music changes tempo when the 6th line from the bottom is reached.
- Pressing up speeds up the piece
- B Game random data shows up at the top instead of the bottom

Many many many thanks to CelestialAmber for the disassembly and meatfighter for the blogpost. 

The original readme:

# Tetris

This is a disassembly of Tetris (NES).

It builds the following rom:

- Tetris (U) [!].nes `md5: ec58574d96bee8c8927884ae6e7a2508`

To set up the repository, see [**INSTALL.md**](INSTALL.md).

Thanks to <https://github.com/ejona86> for creating an info file and other files used to generate the disassembly code and other parts of the disassembly. (Original repository link:  <https://github.com/ejona86/taus>)

CHR png converting tools repository link: <https://github.com/qalle2/nes-util>
