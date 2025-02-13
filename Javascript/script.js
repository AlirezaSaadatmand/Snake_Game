const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');

let unit = 15;

let foodX, foodY

let moveX = unit;
let moveY = 0;

let snake = [
    { x: 225 + (unit * 4), y: 225 },
    { x: 225 + (unit * 3), y: 225 },
    { x: 225 + (unit * 2), y: 225 },
    { x: 225 + unit, y: 225 },
    { x: 225, y: 225 }
];

addEventListener('keydown', changeDirection);


function startGame() {
    nextTick()
    createFood()
    drawFood()
}

function nextTick() {
    if (!endGame()) {
        setTimeout(() => {
            clearBoard();
            drawFood();
            moveSnake();
            drawSnake();
            nextTick();
        }, 100);
    }
};

function endGame() {
    for (let i = 1; i < snake.length; i++) {
        if (snake[0].x === snake[i].x && snake[0].y === snake[i].y) return true;

    }

    const hitLeftWall = snake[0].x < 15;
    const hitRightWall = snake[0].x > canvas.width - 30;
    const hitTopWall = snake[0].y < 15;
    const hitBottomWall = snake[0].y > canvas.height - 30;

    return hitLeftWall || hitRightWall || hitTopWall || hitBottomWall;
}

function randomNumber(max, min) {
    return Math.round((Math.random() * (max - min) + min) / 15) * 15
};

function createFood() {
    foodX = randomNumber(0, canvas.width - 15);
    foodY = randomNumber(0, canvas.height - 15);


    snake.forEach(snakePart => {
        if (snakePart.x === foodX && snakePart.y === foodY) {
            createFood();
        }
    })
};

function drawFood() {
    c.fillStyle = 'brown';
    c.strokeStyle = 'black';
    c.lineWidth = 1;
    c.fillRect(foodX, foodY, unit, unit);
    c.strokeRect(foodX, foodY, unit, unit);
};

function clearBoard() {
    c.fillStyle = 'white';
    c.fillRect(0, 0, canvas.width, canvas.height);
}

function drawSnake() {
    let head1 = { x: snake[0].x, y: snake[0].y };

    snake.forEach(part => {
        if (part.x == head1.x && part.y == head1.y) {
            c.lineWidth = 2;
            c.fillStyle = 'black';
            c.strokeStyle = 'black';
            c.fillRect(part.x, part.y, unit, unit);
            c.strokeRect(part.x, part.y, unit, unit);
        } else {
            c.lineWidth = 2;
            c.fillStyle = 'green';
            c.strokeStyle = 'black';
            c.fillRect(part.x, part.y, unit, unit);
            c.strokeRect(part.x, part.y, unit, unit);

        }

    });
};

function moveSnake() {

    const head1 = { x: snake[0].x + moveX, y: snake[0].y + moveY };
    snake.unshift(head1);

    let touch = (snake[0].x == foodX && snake[0].y == foodY);


    if (touch) {
        createFood()

    } else {
        snake.pop();

    }
};

function changeDirection() {
    const keyDown = event.keyCode;

    const LEFT = 37;
    const RIGHT = 39;
    const UP = 38;
    const DOWN = 40;

    const goingUp = (moveY == -unit);
    const goingDown = (moveY == unit);
    const goingRight = (moveX == unit);
    const goingLeft = (moveX == -unit);




    if (keyDown == UP && !goingDown) {
        moveX = 0;
        moveY = -unit;
    }
    if (keyDown == DOWN && !goingUp) {
        moveX = 0;
        moveY = unit;
    }
    if (keyDown == RIGHT && !goingLeft) {
        moveX = unit;
        moveY = 0;
    }
    if (keyDown == LEFT && !goingRight) {
        moveX = -unit;
        moveY = 0;
    }
}
startGame()