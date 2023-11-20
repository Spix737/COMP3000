// Init canvas and some other important global variables.
let socket = null;

// Variables for drawing hexagons.
const a = 2 * Math.PI / 6;

// Default Catan layout
const tile_colors = {'hills': '#fa914f', 'forest': '#187b13', 'pasture': '#5ee557', 'mountains': '#9d998f', 'fields': '#fbf250', 'desert': '#fcf799', 'none': 'white'}
const default_tiles = ['mountains', 'pasture', 'forest',
                       'fields', 'hills', 'pasture', 'hills',
                       'fields', 'forest', 'desert', 'forest', 'mountains',
                       'forest', 'mountains', 'fields', 'pasture',
                       'hills', 'fields', 'pasture']
const default_tokens = [10, 2, 9,
                        12, 6, 4, 10,
                        9, 11, 7, 3, 8,
                        8, 3, 4, 5,
                        5, 6, 11]
const tiles = ['none', 'none', 'none',
               'none', 'none', 'none', 'none',
               'none', 'none', 'none', 'none', 'none',
               'none', 'none', 'none', 'none',
               'none', 'none', 'none']
const tokens = [null, null, null,
                null, null, null, null,
                null, null, null, null, null,
                null, null, null, null,
                null, null, null]
const neg_tiles = [[], [], [],
                   [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [],
                   [], [], []]
const neg_tokens = [[], [], [],
                    [], [], [], [],
                    [], [], [], [], [],
                    [], [], [], [],
                    [], [], []]
const next_tile = {'none': 'hills', 'hills': 'forest', 'forest': 'mountains', 'mountains': 'fields', 'fields': 'pasture', 'pasture': 'desert', 'desert': 'none'}
const coordinates = [[0, -2], [1, -2], [2, -2],
                     [-1, -1], [0, -1], [1, -1], [2, -1],
                     [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0],
                     [-2, 1], [-1, 1], [0, 1], [1, 1],
                     [-2, 2], [-1, 2], [0, 2]]
highlightTile = null
extra_constraints = {'centerdesert': false, 'neighbourtoken': false, 'neighbourtile': false,
                    'balanceprob': false, 'elevenpips': false}
                    

function axialCoordToTileId(q, r) {
  // If invalid, return null.
  if (Math.abs(q + r) > 2) {
    return null;
  }
  let idx = null
  if (r == -2) {
    idx = Math.abs(q);
  } else if (r == -1) {
    idx = q + 4;
  } else if (r == 0) {
    idx = q + 9;
  } else if (r == 1) {
    idx = q + 14;
  } else if (r == 2) {
    idx = q + 18;
  }
  return idx;
}

function coordToTile(x, y) {
  // Convert x y coordinates of canvas to the tile's ID.
  // const center_x = WIDTH/2;
  // const center_y = HEIGHT/2;
  // const radius = WIDTH/7/2;

  x -= WIDTH/2;
  y -= 2*HEIGHT/3;

  // TODO: properly round
  const q = Math.round((Math.sqrt(3)/3 * x - 1.0/3 * y) / radius);
  const r = Math.round((2.0/3 * y) / radius);


  let idx = axialCoordToTileId(q, r)
  return idx;
}

function buttonClicked(x, y) {
  // Function which tries to find what button in the toolbar was clicked.
  // The hit detection use square approximations of the real buttons. As such, it is not precise. :-)
  // console.log(x, y)
  // console.log(HEIGHT/8)
  // console.log(HEIGHT/8 * 2)
  const tiles_center = HEIGHT/8
  if (tiles_center - radius <= y && y <= tiles_center + radius) {
    // One of the toolbar tiles was clicked.
    // Change the tile type of the highlit tile.
    const tile_idx = Math.round(x/(WIDTH/8));
    let tile_type = null;
    if (tile_idx === 1) {
      tile_type = 'hills';
    } else if (tile_idx === 2) {
      tile_type = 'forest';
    } else if (tile_idx === 3) {
      tile_type = 'pasture';
    } else if (tile_idx === 4) {
      tile_type = 'mountains';
    } else if (tile_idx === 5) {
      tile_type = 'fields';
    } else if (tile_idx === 6) {
      tile_type = 'desert';
    } else if (tile_idx === 7) {
      tile_type = 'none';
    }
    // Only set the tile type if it is allowed, else explain why it isn't.
    if (!neg_tiles[highlightTile].includes(tile_type)) {
        tiles[highlightTile] = tile_type;
    } else {
        prev_type = tiles[highlightTile]
        tiles[highlightTile] = tile_type;
        explain()
        tiles[highlightTile] = prev_type;
    }
  } else {
    // One of the toolbar tokens was clicked.
    // Change the token of the highlit tile.
    token_idx = Math.round(x/(WIDTH/13));
    console.log(token_idx);
    let token = null
    if (token_idx !== 6) {
      // We only set the token if it was not a seven.
      token = token_idx + 1
    }
    // Only set the tile token if it is allowed, else explain why it isn't.
    if (!neg_tokens[highlightTile].includes(token)) {
        tokens[highlightTile] = token;
    } else {
        prev_token = tokens[highlightTile];
        tokens[highlightTile] = token;
        explain()
        tokens[highlightTile] = prev_token;
    }
  }
}

function clickHandler(e) {
  // Check if the toolbar was clicked, or the grid.
  if (e.clientY < HEIGHT/3) {
    // If the toolbar was clicked, we need to update.
    buttonClicked(e.clientX, e.clientY);

    if (document.getElementById('autopropagate').checked) {
      propagate();
    }
  } else {
    // Find which plane was clicked, color it & update total score.
    tile = coordToTile(e.clientX, e.clientY);
    highlightTile = tile
  }
  drawBoard();
}

/*
 * Display a model in the grid.
 */
function showGrid(model) {
  // We need to set the tile types and the tile tokens.
  for (var i in model['tile_type']) {
    let coords = i;
    // Remove parenthesis
    coords = coords.replace(/\)/g, '').replace(/\(/g, '').replace(/'/g, '');
    coords = coords.split(', ');
    coords = coords.map(Number);
    const q = coords[0];
    const r = coords[1];
    const idx = axialCoordToTileId(q, r);
    tiles[idx] = model['tile_type'][i];
    tokens[idx] = Number(model['tile_token'][i]);
  }
  drawBoard()
}

/* 
 * Set the negative values (i.e., values that are impossible) based on a negdict.
 */
function setNeg(negDict) {
  for (var i in negDict['tile_type']) {
    let coords = i;
    coords = coords.replace(/\)/g, '').replace(/\(/g, '').replace(/'/g, '');
    coords = coords.split(', ');
    coords = coords.map(Number);
    const q = coords[0];
    const r = coords[1];
    const idx = axialCoordToTileId(q, r);
    neg_tiles[idx] = negDict['tile_type'][i]
  }
  for (var i in negDict['tile_token']) {
    let coords = i;
    coords = coords.replace(/\)/g, '').replace(/\(/g, '').replace(/'/g, '');
    coords = coords.split(', ');
    coords = coords.map(Number);
    const q = coords[0];
    const r = coords[1];
    const idx = axialCoordToTileId(q, r);
    neg_tokens[idx] = negDict['tile_token'][i].map(Number);
    console.log(negDict['tile_token'])
  }
}

/*
 * Set the propagated values.
 */
function setPos(posDict) {
  for (var i in posDict['tile_type']) {
    let coords = i;
    coords = coords.replace(/\)/g, '').replace(/\(/g, '').replace(/'/g, '');
    coords = coords.split(', ');
    coords = coords.map(Number);
    const q = coords[0];
    const r = coords[1];
    const idx = axialCoordToTileId(q, r);
    if (idx === null) {
      continue;
    }
    tiles[idx] = posDict['tile_type'][i];
  }
  for (var i in posDict['tile_token']) {
    let coords = i;
    coords = coords.replace(/\)/g, '').replace(/\(/g, '').replace(/'/g, '');
    coords = coords.split(', ');
    coords = coords.map(Number);
    const q = coords[0];
    const r = coords[1];
    const idx = axialCoordToTileId(q, r);
    if (idx === null) {
      continue;
    }
    tokens[idx] = Number(posDict['tile_token'][i]);
  }
}

function showExplain(bool, explain) {
  if (bool) {
    document.getElementById('explain').innerHTML = explain.replace(/\n/g, "<br/>");
    document.getElementById('explainBox').style.visibility = 'visible';
  } else {
    document.getElementById('explain').innerHTML = ''
    document.getElementById('explainBox').style.visibility = 'hidden';
  }
}

// IDP related stuff.
function initKb() {
  voc = `
vocabulary {
    type Q := {-2..2}
    type R := {-2..2}
    type Tile := {hills, forest, mountains, fields, pasture, desert, none}
    type Token := {1..12}
    type Pips := {0..5}
    
    tile_type : (Q * R) -> Tile
    tile_token : (Q * R) -> Token
    neighbour : (Q * R * Q * R) -> Bool
    relevant : (Q * R) -> Bool

    token_pips: (Token) -> Pips
}`

  struct = `
structure {
    token_pips := {
        2 -> 1, 12 -> 1,
        3 -> 2, 11 -> 2,
        4 -> 3, 10 -> 3,
        5 -> 4, 9 -> 4,
        6 -> 5, 8 -> 5,
        7 -> 0, 1 -> 0
    }.
    neighbour := {(-2,0,-2,1), (-2,0,-1,-1), (-2,0,-1,0), (-2,0,-1,1), (-2,1,-2,0), (-2,1,-2,2), (-2,1,-1,0), (-2,1,-1,1), (-2,1,-1,2), (-2,2,-2,1), (-2,2,-1,1), (-2,2,-1,2), (-1,-1,-2,0), (-1,-1,-1,0), (-1,-1,0,-2), (-1,-1,0,-1), (-1,-1,0,0), (-1,0,-2,0), (-1,0,-2,1), (-1,0,-1,-1), (-1,0,-1,1), (-1,0,0,-1), (-1,0,0,0), (-1,0,0,1), (-1,1,-2,0), (-1,1,-2,1), (-1,1,-2,2), (-1,1,-1,0), (-1,1,-1,2), (-1,1,0,0), (-1,1,0,1), (-1,1,0,2), (-1,2,-2,1), (-1,2,-2,2), (-1,2,-1,1), (-1,2,0,1), (-1,2,0,2), (0,-2,-1,-1), (0,-2,0,-1), (0,-2,1,-2), (0,-2,1,-1), (0,-1,-1,-1), (0,-1,-1,0), (0,-1,0,-2), (0,-1,0,0), (0,-1,1,-2), (0,-1,1,-1), (0,-1,1,0), (0,0,-1,-1), (0,0,-1,0), (0,0,-1,1), (0,0,0,-1), (0,0,0,1), (0,0,1,-1), (0,0,1,0), (0,0,1,1), (0,1,-1,0), (0,1,-1,1), (0,1,-1,2), (0,1,0,0), (0,1,0,2), (0,1,1,0), (0,1,1,1), (0,2,-1,1), (0,2,-1,2), (0,2,0,1), (0,2,1,1), (1,-2,0,-2), (1,-2,0,-1), (1,-2,1,-1), (1,-2,2,-2), (1,-2,2,-1), (1,-1,0,-2), (1,-1,0,-1), (1,-1,0,0), (1,-1,1,-2), (1,-1,1,0), (1,-1,2,-2), (1,-1,2,-1), (1,-1,2,0), (1,0,0,-1), (1,0,0,0), (1,0,0,1), (1,0,1,-1), (1,0,1,1), (1,0,2,-1), (1,0,2,0), (1,1,0,0), (1,1,0,1), (1,1,0,2), (1,1,1,0), (1,1,2,0), (2,-2,1,-2), (2,-2,1,-1), (2,-2,2,-1), (2,-1,1,-2), (2,-1,1,-1), (2,-1,1,0), (2,-1,2,-2), (2,-1,2,0), (2,0,1,-1), (2,0,1,0), (2,0,1,1), (2,0,2,-1)}.
    relevant := {(-2,0), (-2,1), (-2,2), (-1,-1), (-1,0), (-1,1), (-1,2), (0,-2), (0,-1), (0,0), (0,1), (0,2), (1,-2), (1,-1), (1,0), (1,1), (2,-2), (2,-1), (2,0)}.
         
}
`

  theory = `
theory {

    // Set invalid tile coordinates as "none", with token value 1.
    !q in Q, r in R: ~relevant(q, r) <=> tile_type(q, r) = none.
    !q in Q, r in R: ~relevant(q, r) <=> tile_token(q, r) = 1.
    
    // Set the occurrence of each tile type.
    #{q in Q, r in R: tile_type(q, r) = pasture} = 4.
    #{q in Q, r in R: tile_type(q, r) = fields} = 4.
    #{q in Q, r in R: tile_type(q, r) = forest} = 4.
    #{q in Q, r in R: tile_type(q, r) = hills} = 3.
    #{q in Q, r in R: tile_type(q, r) = mountains} = 3.
    #{q in Q, r in R: tile_type(q, r) = desert} = 1.

    // Set the occurrence of each number token.
    #{q in Q, r in R: tile_token(q, r) = 2} = 1.
    #{q in Q, r in R: tile_token(q, r) = 3} = 2.
    #{q in Q, r in R: tile_token(q, r) = 4} = 2.
    #{q in Q, r in R: tile_token(q, r) = 5} = 2.
    #{q in Q, r in R: tile_token(q, r) = 6} = 2.
    #{q in Q, r in R: tile_token(q, r) = 7} = 1.
    #{q in Q, r in R: tile_token(q, r) = 8} = 2.
    #{q in Q, r in R: tile_token(q, r) = 9} = 2.
    #{q in Q, r in R: tile_token(q, r) = 10} = 2.
    #{q in Q, r in R: tile_token(q, r) = 11} = 2.
    #{q in Q, r in R: tile_token(q, r) = 12} = 1.

    // The desert always gets token 7.
    [The desert always gets token 7]
    !q in Q, r in R: tile_token(q, r) = 7 => tile_type(q, r) = desert.
    
    `
  // We have a list of extra constraints that can be added.
  if (document.getElementById('centerdesert').checked) {
    theory += `
    [The desert is always in the center]
    tile_type(0, 0) = desert.
    `
  }
  if (document.getElementById('neighbourtoken').checked) {
    theory += `
    [Two neighbouring tiles may not have the same token]
    !q1, q2 in Q, r1, r2 in R: neighbour(q1, r1, q2, r2) => tile_token(q1, r1) ~= tile_token(q2, r2).
      `
  }
  if (document.getElementById('neighbourtile').checked) {
    theory += `
    [Two neighbouring tiles may not have the same resource]
    !q1, q2 in Q, r1, r2 in R: neighbour(q1, r1, q2, r2) => tile_type(q1, r1) ~= tile_type(q2, r2).
    `
  }
  if (document.getElementById('balanceprob').checked) {
    theory += `
    // Balance the low probability tokens over the resources.
    !t in Tile: t = pasture | t = fields | t = forest => #{q in Q, r in R: tile_type(q, r) = t & token_pips(tile_token(q, r)) =< 2} < 3.
    !t in Tile: t = hills | t = mountains => #{q in Q, r in R: tile_type(q, r) = t & token_pips(tile_token(q, r)) =< 2} < 2.
    `
  }
  if (document.getElementById('elevenpips').checked) {
    theory += `
    // Each intersection may not contain more than 11 pips (they should not be too fruitful!)
    !q1, q2, q3 in Q, r1, r2, r3 in R: neighbour(q1, r1, q2, r2) & neighbour(q1, r1, q3, r3) & neighbour(q2, r2, q3, r3) => token_pips(tile_token(q1, r1)) + token_pips(tile_token(q2, r2)) + token_pips(tile_token(q3, r3)) =<  11.
`
  }

  for (let i = 0; i < tiles.length; i++) {
    if (tiles[i] !== 'none') {
      const q = coordinates[i][0]
      const r = coordinates[i][1]
      theory += 'tile_type(' + q + ',' + r + ') = ' + tiles[i] + '.\n';
    }
    if (tokens[i] !== null) {
      const q = coordinates[i][0]
      const r = coordinates[i][1]
      theory += 'tile_token(' + q + ',' + r + ') = ' + tokens[i] + '.\n';
    }
  }

  // Add tiles already configured by the user.


  theory += `}`

  socket.send(JSON.stringify({'method': 'create',
                              'theory': voc + theory + struct}));
}

function initSocket() {
  //socket = new WebSocket("ws://localhost:8765");
  socket = new WebSocket("wss:websocket.simonvandevelde.be");

  socket.onopen = function(e) {
    initKb();
  }
  socket.onmessage = function(event) {
    showExplain(false, '');
    data = JSON.parse(event.data);
    if (data['method'] === 'modelexpand') {
      if (data['success']) {
        showGrid(data['models'][0]);
        loading(false);
      } else {
        explain()
			  console.log(data);
      }
    } else if (data['method'] === 'propagate') {
      setNeg(data['negdict'])
      setPos(data['posdict'])
      console.log(data['negdict'])
      drawBoard();
      if (Object.keys(data['negdict']['tile_token']).length) {
        loading(false);
      }
    } else if (data['method'] === 'explain') {
      showExplain(true, data['explanation'])
      loading(false);
    } else {
    }
  }
}


function modelExpand() {
  // Re-initialize the KB with new constraints
  loading(true);
  initKb();
  msg = {'method': 'modelexpand',
         'number': 1};
  console.log(msg);
  socket.send(JSON.stringify(msg));
}

function propagate() {
  loading(true);
  initKb();
  msg = {'method': 'propagate',
         'symbol': 'tile_type'}
  socket.send(JSON.stringify(msg));
  loading(true);
  msg = {'method': 'propagate',
         'symbol': 'tile_token'}
  socket.send(JSON.stringify(msg));
}

function explain() {
  loading(true);
  initKb();
  msg = {'method': 'explain'}
  socket.send(JSON.stringify(msg));
}

function reset() {
  for (let i = 0; i < tiles.length; i++) {
    tiles[i] = 'none';
    tokens[i] = null;
    neg_tiles[i] = [];
    neg_tokens[i] = [];
  }
  drawBoard();
}
  

initSocket()
