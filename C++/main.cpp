#include <iostream>
#include "raylib.h"
#include <vector>

const int WIDTH = 1200;
const int HEIGHT = 700;

const int UNIT = 25;
int score = 0;

Vector2 food;

int createFood(std::vector<Vector2> parts , Vector2& food) {
    int x = GetRandomValue(0 , WIDTH / UNIT - 1);
    int y = GetRandomValue(0 , HEIGHT / UNIT - 1);

    for (auto part : parts) {
        if (part.x == x * UNIT && part.y == y * UNIT) {
            createFood(parts, food);
            return 0;
        }
    }
    food = {x * UNIT, y * UNIT};
    return 1;
}

class Snake {
    public:
        std::vector<Vector2> parts;
        bool up = false;
        bool down = false;
        bool right = false;
        bool left = false;

        int size = 3;

        Snake() {
            parts.push_back({4 * UNIT , 4 * UNIT});
            // parts.push_back({5 * UNIT , 4 * UNIT});
            // parts.push_back({6 * UNIT , 4 * UNIT});
        }

        void reset() {
            up = false;
            down = false;
            right = false;
            left = false;
        }

        void Move() {
            if ((IsKeyDown(KEY_W) || IsKeyDown(KEY_UP)) && !down){
                reset();
                up = true;
            } else if ((IsKeyDown(KEY_S) || IsKeyDown(KEY_DOWN)) && !up){
                reset();
                down = true;
            } else if ((IsKeyDown(KEY_A) || IsKeyDown(KEY_LEFT)) && !right){
                reset();                
                left = true;
            } else if ((IsKeyDown(KEY_D) || IsKeyDown(KEY_RIGHT)) && !left){
                reset();                
                right = true;
            }
            Vector2 part = {parts[0].x , parts[0].y};
            if (up) { part.y -= UNIT; }
            else if (down) { part.y += UNIT; }
            else if (right) { part.x += UNIT; }
            else if (left) { part.x -= UNIT; }

            if (part.x == food.x && part.y == food.y){
                size++;
                score++;
                createFood(parts , food);
            } else {
                parts.erase(parts.begin() + size);
            }
            parts.insert(parts.begin(), part);
            
        }

        void Draw() {
            for (int i = 0 ; i < parts.size() ; i++){
                DrawRectangle(parts[i].x , parts[i].y , UNIT , UNIT , Color{0, 255, 0, 255});
                DrawRectangleLines(parts[i].x, parts[i].y, UNIT, UNIT, BROWN);
            }
        }
};

int checkEndGame(std::vector<Vector2>& parts){
    Vector2 head = parts[0];
    if (head.x < 0 || head.x > WIDTH || head.y < 0 || head.y > HEIGHT){
        return 1;
    }
    for (int i = 1 ; i < parts.size() ; i++){
        if (head.x == parts[i].x && head.y == parts[i].y){
            return 1;
        }
    }
    return 0;
}

int main(){

    InitWindow(WIDTH , HEIGHT , "Snake game");
    SetTargetFPS(15);


    Snake snake;

    createFood(snake.parts , food);

    while(!WindowShouldClose()) {


        BeginDrawing();
        DrawRectangle(0, 0, WIDTH, HEIGHT, Color{0, 0, 0, 250});

        DrawText(TextFormat("Score: %d", score), 20, 20, 30, WHITE);
        DrawRectangle(food.x , food.y , UNIT , UNIT , Color{255, 0, 0, 255});
        
        
        snake.Move();
        snake.Draw();
        EndDrawing();
        if (checkEndGame(snake.parts)){
            break;
        }  
    }
    CloseWindow();
    return 0;
}