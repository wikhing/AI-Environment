package pong;

import javafx.animation.Animation;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Paint;
import javafx.scene.text.Font;
import javafx.scene.text.TextAlignment;
import javafx.stage.Stage;
import javafx.util.Duration;
import javafx.scene.Group;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

/**
 * JavaFX App
 */
public class App extends Application {
    // Bar position, ball position and velocity, score

    private HashMap<String, Boolean> currentlyActiveKeys = new HashMap<>();
    private Scene scene;
    Timeline timeline;
    boolean hitWall = false;
    boolean pause = false;
    int scoreLeft = 0, scoreRight = 0;      //score

    @Override
    public void start(Stage stage) throws Exception {
        Group groupObj = new Group();
        scene = new Scene(groupObj, 500, 500);
        stage.setScene(scene);
        Canvas canvas = new Canvas(500, 500);
        groupObj.getChildren().add(canvas);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        scene.setOnKeyPressed(event -> {
            String codeString = event.getCode().toString();
            if (!currentlyActiveKeys.containsKey(codeString)) {
                currentlyActiveKeys.put(codeString, true);
            }

            if (codeString.equals("P")) {
                if(pause){
                    timeline.play();
                    pause = false;
                }else{
                    timeline.pause();
                    pause = true;
                }
            }else if(codeString.equals("SPACE")){
                xBall = 30;
                yBall = 240;
                xVector = 5;
                yVector = 2;
                bar1 = 230;
                bar2 = 230;
                hitWall = false;
                timeline.playFromStart();
            }
        });
        scene.setOnKeyReleased(event2 -> {
            currentlyActiveKeys.remove(event2.getCode().toString());
        });


        

        timeline = new Timeline(new KeyFrame(Duration.seconds(0.04), e -> {
            ballMovement(gc);
            barMove(gc);
            gc.setTextAlign(TextAlignment.CENTER);
            gc.setFont(Font.font("arial", 20));
            gc.fillText("Player 1 Score: " + scoreLeft, 160, 20);
            gc.fillText("Player 2 Score: " + scoreRight, 340, 20);

            if(xBall >= 455 || xBall <= 25){
                gc.setFill(Paint.valueOf("red"));
            }else{
                gc.setFill(Paint.valueOf("black"));
            }

            
            //To JSon
            Gson gson = new Gson();
            JsonObject jsonObject = new JsonObject();
            jsonObject.addProperty("Ball Pos X", xBall);
            jsonObject.addProperty("Ball Pos Y", yBall);
            jsonObject.addProperty("Ball Vector X", xVector);
            jsonObject.addProperty("Ball Vector Y", yVector);
            jsonObject.addProperty("Bar Pos 1", bar1);
            jsonObject.addProperty("Bar Pos 2", bar2);
            jsonObject.addProperty("Score Left", scoreLeft);
            jsonObject.addProperty("Score Right", scoreRight);
            jsonObject.addProperty("Wall is hit", hitWall);
            jsonObject.addProperty("Game is paused", pause);
            String json = gson.toJson(jsonObject);

            try {
                FileWriter file = new FileWriter("Pong_Java\\pong\\2PlyerPong.json", false);
                file.write(json + "\n");
                file.close();
            } catch (IOException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            }


            // try {
            //     BufferedReader reader = new BufferedReader(new FileReader("2PlyerPong.json"));
            //     String r = reader.readLine();
            //     System.out.println(r);
            //     reader.close();
            // } catch (FileNotFoundException e1) {
            //     e1.printStackTrace();
            // } catch (IOException e1) {
            //     e1.printStackTrace();
            // }
        }));
        timeline.setCycleCount(Animation.INDEFINITE);
        timeline.playFromStart();

        stage.show();
    }

    int xAxis = 0, yAxis = 0;
    int xBall = 30, yBall = 240, xVector = 5, yVector = 2;          //ball position and velocity
    int bar1 = 230, bar2 = 230;                                     //bar position

    private void ballMovement(GraphicsContext gc) {
        gc.clearRect(0, 0, 500, 500);
        
        //ball hit wall
        if (!hitWall && xBall <= 0) {           //Right win
            xVector = 0;
            yVector = 0;
            hitWall = true;
            scoreRight++;
        }else if(!hitWall && xBall >= 480){     //Left win
            xVector = 0;
            yVector = 0;
            hitWall = true;
            scoreLeft++;
        }

        if (yBall <= 0 || yBall >= 480) {
            yVector = -yVector;
        }

        if(hitWall){
            gc.setFont(Font.font("arial", 50));
            gc.fillText("GAME OVER", 250, 250);
            return;
        }

        //ball hit bar
        if (xBall <= 25 && ((yBall >= bar1 && yBall <= bar1 + 40) || yBall + 20 >= bar1 && yBall + 20 <= bar1 + 40)) {
            xVector = Math.abs(xVector);

            currentlyActiveKeys.forEach((k, v) -> {
                if (v) {
                    switch (k) {
                        case "W":
                            yVector = ((int)(Math.random() * 2) + Math.abs(yVector)) * -1;
                            break;
                        case "S":
                            yVector = ((int)(Math.random() * 2) + Math.abs(yVector));
                            break;
                    }
                }
            });
        }
        if (xBall >= 455 && ((yBall >= bar2 && yBall <= bar2 + 40) || yBall + 20 >= bar2 && yBall + 20 <= bar2 + 40)) {
            xVector = Math.abs(xVector) * -1;

            currentlyActiveKeys.forEach((k, v) -> {
                if (v) {
                    switch (k) {
                        case "UP":
                                yVector = ((int)(Math.random() * 2) + Math.abs(yVector)) * -1;
                            break;
                        case "DOWN":
                                yVector = ((int)(Math.random() * 2) + Math.abs(yVector));
                            break;
                    }
                }
            });
        }

        xBall += xVector;
        yBall += yVector;

        gc.fillOval(xBall, yBall, 20, 20);
    }

    private void barMove(GraphicsContext gc){

        currentlyActiveKeys.forEach((k, v) -> {
            if (v) {
                switch (k) {
                    case "W":
                        if(bar1 > 0){
                            bar1 -= 5;
                        }
                        break;
                    case "S":
                        if(bar1 < 460){
                            bar1 += 5;
                        }
                        break;
                    case "UP":
                        if(bar2 > 0){
                            bar2 -= 5;
                        }
                        break;
                    case "DOWN":
                        if(bar2 < 460){
                            bar2 += 5;
                        }
                        break;
                }
            }
        });

        gc.fillRect(20, bar1, 5, 40);
        gc.fillRect(475, bar2, 5, 40);
    }

    public static void main(String[] args) {
        launch(args);
    }
}