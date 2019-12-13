package com.company;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Server {
    public static void main(String[] args) {

        ServerSocket ss = null;
        try {
            ss = new ServerSocket(19955);
        } catch (IOException e) {
            e.printStackTrace();
        }
        while(true){
            try {
                System.out.println("waiting...");
                Socket socket = ss.accept();
                System.out.println("client connected: " + socket.getInetAddress().getHostAddress());
                ClientHandler ch = new ClientHandler(socket);
                ch.start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
