package main

import (
	"fmt"
	"image/color"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const UNIT = 25
const WIDTH = 1200
const HEIGHT = 700

var score = 0
var gameOver = false

var foodX int
var foodY int

type Snake struct {
	parts      []Part
	goingUp    bool
	goingDown  bool
	goingRight bool
	goingLeft  bool
}

type Part struct {
	x int
	y int
}

func resetMove(snake *Snake) {
	snake.goingUp = false
	snake.goingDown = false
	snake.goingRight = false
	snake.goingLeft = false
}

func snakeMove(snake *Snake) {
	if gameOver {
		return
	}

	if (rl.IsKeyDown(rl.KeyUp) || rl.IsKeyDown(rl.KeyW)) && !snake.goingDown {
		resetMove(snake)
		snake.goingUp = true
	} else if (rl.IsKeyDown(rl.KeyDown) || rl.IsKeyDown(rl.KeyS)) && !snake.goingUp {
		resetMove(snake)
		snake.goingDown = true
	} else if (rl.IsKeyDown(rl.KeyRight) || rl.IsKeyDown(rl.KeyD)) && !snake.goingLeft {
		resetMove(snake)
		snake.goingRight = true
	} else if (rl.IsKeyDown(rl.KeyLeft) || rl.IsKeyDown(rl.KeyA)) && !snake.goingRight {
		resetMove(snake)
		snake.goingLeft = true
	}

	head := snake.parts[len(snake.parts)-1]

	if snake.goingUp {
		head.y -= UNIT
	} else if snake.goingDown {
		head.y += UNIT
	} else if snake.goingRight {
		head.x += UNIT
	} else if snake.goingLeft {
		head.x -= UNIT
	}

	gameOver = checkCollistion(*snake, head)

	if head.x == foodX && head.y == foodY {
		score++
		createFood(*snake)
	} else {
		snake.parts = snake.parts[1:]
	}
	snake.parts = append(snake.parts, head)

}

func createFood(snake Snake) {
	x := int(rl.GetRandomValue(0, WIDTH/UNIT-1)) * UNIT
	y := int(rl.GetRandomValue(0, HEIGHT/UNIT-1)) * UNIT

	for _, part := range snake.parts {
		if part.x == x && part.y == y {
			createFood(snake)
			return
		}
	}
	foodX = x
	foodY = y
}

func checkCollistion(snake Snake, head Part) bool {
	if head.x < 0 || head.x >= WIDTH || head.y < 0 || head.y >= HEIGHT {
		return true
	}

	for i := 0; i < len(snake.parts)-1; i++ {
		if head.x == snake.parts[i].x && head.y == snake.parts[i].y {
			return true
		}
	}
	return false
}

func reset(snake *Snake) {
	snake.parts = []Part{
		{x: UNIT * 3, y: UNIT * 3},
		{x: UNIT * 4, y: UNIT * 3},
		{x: UNIT * 5, y: UNIT * 3},
	}
	resetMove(snake)
	snake.goingRight = true

	gameOver = false
	score = 0
	createFood(*snake)
}

func main() {

	snake := Snake{}

	reset(&snake)

	createFood(snake)

	rl.InitWindow(WIDTH, HEIGHT, "Snake Game")
	rl.SetTargetFPS(15)
	defer rl.CloseWindow()

	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.ClearBackground(color.RGBA{34, 40, 49, 255})

		if gameOver {
			rl.DrawText("GAME OVER!", WIDTH/2-120, HEIGHT/2-50, 40, rl.Red)
			rl.DrawText("Press SPACE to Restart", WIDTH/2-120, HEIGHT/2, 20, rl.White)

			if rl.IsKeyDown(rl.KeySpace) {
				reset(&snake)
			}
		} else {
			rl.DrawRectangle(int32(foodX), int32(foodY), UNIT, UNIT, color.RGBA{255, 0, 0, 255})

			rl.DrawText(fmt.Sprintf("Score: %d", score), 20, 20, 30, rl.White)

			snakeMove(&snake)
			for i := 0; i < len(snake.parts); i++ {
				partColor := color.RGBA{0, 255, 0, 255}
				if i == len(snake.parts)-1 {
					partColor = color.RGBA{0, 0, 0, 255}
				}
				rl.DrawRectangle(int32(snake.parts[i].x), int32(snake.parts[i].y), int32(UNIT), int32(UNIT), partColor)
				rl.DrawRectangleLines(int32(snake.parts[i].x), int32(snake.parts[i].y), int32(UNIT), int32(UNIT), color.RGBA{0, 0, 0, 255})
			}
		}

		rl.EndDrawing()
	}
}
