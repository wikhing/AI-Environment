module pong {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.graphics;
    requires java.desktop;
    requires javafx.base;
    requires com.google.gson;

    opens pong to javafx.fxml;
    exports pong;
}
