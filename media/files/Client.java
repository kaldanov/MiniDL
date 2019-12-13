    package com.company;

    import java.io.IOException;
    import java.io.ObjectInputStream;
    import java.io.ObjectOutputStream;
    import java.net.Socket;
    import java.util.Scanner;

    public class Client {
        public static void main(String[] args) {
            try {
                Scanner in = new Scanner(System.in);
                while (true) {
                    Socket socket = new Socket("localhost", 19955);
                    ObjectOutputStream oos = new ObjectOutputStream(socket.getOutputStream());
                    ObjectInputStream ois = new ObjectInputStream(socket.getInputStream());

                    System.out.println("[1] Log in");
                    System.out.println("[2] Registration");
                    System.out.println("[0] Exit");
                    int a = in.nextInt();
                    if (a == 1) {
                        System.out.println("Enter Login:");
                        String login = in.next();
                        System.out.println("Enter Password");
                        String password = in.next();

                        Request request = new Request("LOGIN", new User(null, login, password));
                        oos.writeObject(request);

                        Request request1 = (Request) ois.readObject();

                        if (request1.getOperationType().equals("Correct")) {
                            User this_user = request1.getUser();
                            while (true) {
                                System.out.println("WELCOME " + this_user.getLogin() + "!");
                                System.out.println("[1] Edit login");
                                System.out.println("[2] Change password");
                                System.out.println("[3] Delete account");
                                System.out.println("[0] Exit");
                                int choice = in.nextInt();
                                if (choice == 1){
                                    System.out.println("Enter new login: ");
                                    String login_edit = in.next();
                                    this_user.setLogin(login_edit);
                                    oos.writeObject(new Request("EDIT_LOGIN" , this_user));
                                    Request r = (Request) ois.readObject();
                                    System.out.println(r.getOperationType() + "!");
                                }
                                else if(choice == 2){
                                    System.out.println("Enter new password: ");
                                    String password_edit = in.next();
                                    this_user.setPassword(password_edit);
                                    oos.writeObject(new Request("EDIT_PASSWORD" , this_user));
                                    Request r = (Request) ois.readObject();
                                    System.out.println(r.getOperationType() + "!");
                                }
                                else if(choice == 3){
                                    System.out.println("Tochno hotite udalit?");
                                    System.out.println("[1] Yes");
                                    System.out.println("[2] No");
                                    int del_acc = in.nextInt();
                                    if (del_acc == 1){
                                        oos.writeObject(new Request("DELETE_THIS_ACC" , this_user));
                                        Request r = (Request) ois.readObject();
                                        System.out.println(r.getOperationType() + "!");
                                        break;
                                    }
                                }
                                else break;
                            }
                        } else {
                            System.out.println("Incorrect login or password!");
                        }
                    }
                    else if (a == 2){
                        System.out.println("Create Login:");
                        String login = in.next();

                        System.out.println("Think Password");
                        String password = in.next();
                        Request request = new Request("ADD", new User(null,login, password));
                        oos.writeObject(request);

                        Request request2 = (Request) ois.readObject();

                        if (request2.getOperationType().equals("ADDED")){
                            System.out.println("Registration successfully!");
                        }
                        else{
                            System.out.println("Registration error!");
                        }
                    }
                    else break;
                }

            } catch (IOException | ClassNotFoundException e) {
                e.printStackTrace();
            }
        }
    }
