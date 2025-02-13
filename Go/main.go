package main

import (
	"fmt"
	"image/color"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const UNIT = 25

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

func reset(snake *Snake) {
	snake.goingUp = false
	snake.goingDown = false
	snake.goingRight = false
	snake.goingLeft = false
}

func snakeMove(snake *Snake) {
	if rl.IsKeyDown(rl.KeyUp) && !snake.goingDown {
		reset(snake)
		snake.goingUp = true
	} else if rl.IsKeyDown(rl.KeyDown) && !snake.goingUp {
		reset(snake)
		snake.goingDown = true
	} else if rl.IsKeyDown(rl.KeyRight) && !snake.goingLeft {
		reset(snake)
		snake.goingRight = true
	} else if rl.IsKeyDown(rl.KeyLeft) && !snake.goingRight {
		reset(snake)
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
	snake.parts = snake.parts[1:]
	snake.parts = append(snake.parts, head)

}

func main() {

	snake := Snake{}
	snake.parts = append(snake.parts, Part{x: UNIT * 3, y: UNIT * 3})
	snake.parts = append(snake.parts, Part{x: UNIT * 4, y: UNIT * 3})
	snake.parts = append(snake.parts, Part{x: UNIT * 5, y: UNIT * 3})
	fmt.Println(snake.parts)

	fmt.Println("hello world")
	rl.InitWindow(1200, 700, "Snake Game")
	rl.SetTargetFPS(15)
	defer rl.CloseWindow()

	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.ClearBackground(rl.Black)
		snakeMove(&snake)
		for i := 0; i < len(snake.parts); i++ {
			rl.DrawRectangle(int32(snake.parts[i].x), int32(snake.parts[i].y), int32(UNIT), int32(UNIT), color.RGBA{255, 0, 0, 255})
		}
		rl.EndDrawing()
	}
}
