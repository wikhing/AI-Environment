        var canvas = document.getElementById('game');
        var score = document.getElementById('score');
        var table = document.getElementById('table');
        var context = canvas.getContext('2d');

        
        for(let i = 0; i < 25; i++){
            var a = document.createElement("a");
            for(let j = 0; j < 25; j++){
                var label = document.createElement("label");
                label.id = i + '@' + j;
                label.textContent = "0 ";
                label.style.color = "white";
                a.appendChild(label);
            }
            table.appendChild(a);
        }
        
        var row = new Array(25);
        var grids = new Array(25);

        var grid = 16;
        var speed = 0;

        var snake = {
            x: 160,
            y: 160,

            dx: grid,
            dy: 0,

            cells:[],

            maxCells: 4
        };

        var apple = {
            x: getRandomInt(0, 25) * grid,
            y: getRandomInt(0, 25) * grid
        };

        function getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min)) + min;
        }

        function loop(){
            requestAnimationFrame(loop);
            
            if(++speed < 8){
                return;
            }

            speed = 0;
            context.clearRect(0, 0, canvas.width, canvas.height);
            row.fill(0);
            for(let i = 0; i < 25; i++){
                grids[i] = row.slice();
            }
            

            snake.x += snake.dx;
            snake.y += snake.dy;

            snake.cells.unshift({x: snake.x, y: snake.y});

            if(snake.cells.length > snake.maxCells){
                var toRemove = snake.cells.pop();
                grids[toRemove.y / 16][toRemove.x / 16] = 0;
            }

            context.fillStyle = 'red';
            context.fillRect(apple.x, apple.y, grid-1, grid-1);
            grids[apple.y / 16][apple.x / 16] = 3;

            context.fillStyle = 'green';
            snake.cells.forEach(function(cell, index) {
                context.fillRect(cell.x, cell.y, grid-1, grid-1);

                if(cell.x === apple.x && cell.y === apple.y){
                    snake.maxCells++;
                    score.innerText = "Score: " + (snake.maxCells - 4);

                    grids[apple.y / 16][apple.x / 16] = 0;

                    apple.x = getRandomInt(0, 25) * grid;
                    apple.y = getRandomInt(0, 25) * grid;

                    grids[apple.y / 16][apple.x / 16] = 3;
                }

                for(var i = index + 1; i < snake.cells.length; i++){
                    
                    if(cell.x === snake.cells[i].x && cell.y === snake.cells[i].y || snake.x < 0 || snake.x >= canvas.width || snake.y < 0 || snake.y >= canvas.height) {
                        snake.x = 160;
                        snake.y = 160;
                        snake.cells = [];
                        snake.maxCells = 4;
                        snake.dx = grid;
                        snake.dy = 0;

                        score.innerText = "Score: 0";

                        grids[apple.y / 16][apple.x / 16] = 0;

                        apple.x = getRandomInt(0, 25) * grid;
                        apple.y = getRandomInt(0, 25) * grid;

                        row.fill(0);
                        for(let i = 0; i < 25; i++){
                            grids[i] = row.slice();
                        }

                        grids[snake.y / 16][snake.x / 16] = 2;
                        grids[apple.y / 16][apple.x / 16] = 3;
                    }
                }
                grids[cell.y / 16][cell.x / 16] = 1;
            });
            grids[snake.y / 16][snake.x / 16] = 2;

            updateTable(grids);
            saveToFile(grids);
        }

        function updateTable(grids){
            for(let i = 0; i < 25; i++){
                for(let j = 0; j < 25; j++){
                    var label = document.getElementById(i+'@'+j);
                    
                    label.innerText = grids[i][j] + " ";
                }
            }
            return;
        }

        function saveToFile(grids){
            let keys = grids.shift();
            let json = grids.map(row => Object.assign({}, ...row.map((col) => ({ col }))));

            const jsonContent = JSON.stringify(json);

            console.log(jsonContent);
            const blob = new Blob([jsonContent], {type: "application/json"});
            saveAs(blob, "snake_data.json");
            // fs.writeFile('snake_data.json', jsonContent, 'utf8', function (err) {
            //     if (err) {
            //         return console.log(err);
            //     }
            // });
        }
        
        document.addEventListener('keydown', function(e) {
            
            if(e.which === 37 && snake.dx === 0){
                snake.dx = -grid;
                snake.dy = 0;
            }

            else if(e.which === 38 && snake.dy === 0){
                snake.dy = -grid;
                snake.dx = 0;
            }

            else if(e.which === 39 && snake.dx === 0){
                snake.dx = grid;
                snake.dy = 0;
            }

            else if(e.which === 40 && snake.dy === 0){
                snake.dy = grid;
                snake.dx = 0;
            }
        });

        requestAnimationFrame(loop);