import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class App {
    /*
     * Objective: Build an interactive terminal-based banking application.
     * Following these step-by-step tasks will let you practice core coding basics
     * (variables, loops, arrays/lists, exception handling) and
     * master Object-Oriented Programming (classes, encapsulation, inheritance,
     * polymorphism, and abstraction)
     * in one clean workflow.
     */
    static Scanner scanner = new Scanner(System.in);
    // If user is admin, username is "admin", password is "admin123"
    // If user is customer, below registrations are valid
    static List<User> users = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        Admin admin = new Admin("admin", "admin123");
        users.add(admin);
        List<Customer> customers = new ArrayList<Customer>();
        seedDatabase(customers);
        welcome();
        login();
        menu(customers.get(0));
    }

    public static User login() {
        System.out.println("Please enter username and password, space separated");
        String input = scanner.nextLine();
        String[] split = input.split(" ");
        String username = split[0];
        String password = split[1];

        for (User user : users) {
            if (user.username.equals(username) && user.password.equals(password)) {
                return user;
            }
        }
        return null;
    }

    public static void welcome() {
        System.out.println("Welcome to ABC Digital Bank");
    }

    public static void menu(Customer customer) {
        int AccountNumber = -1;
        int choice = -1;
        while (choice != 7) {
            System.out.println("1) Create Account");
            System.out.println("2) View All Accounts");
            System.out.println("3) Deposit");
            System.out.println("4) Withdraw");
            System.out.println("5) Transfer");
            System.out.println("6) Close Account");
            System.out.println("7) Exit");

            choice = scanner.nextInt();

            switch (choice) {
                /*
                 * Ask for Account type
                 */
                case 1:
                    scanner.nextLine();
                    System.out.println("1) Checking     2) Saving");
                    int input = scanner.nextInt();
                    Account newAccount = Customer.createAccount(input, customer);
                    newAccount.PrintReceipt();
                    break;
                /*
                 * Iterate through collection and output all active account details
                 */
                case 2:
                    scanner.nextLine();
                    for (Account account : customer.accounts) {
                        account.PrintReceipt();
                    }
                    break;
                /*
                 * call deposit method with amount, and what accoount
                 */
                case 3:
                    scanner.nextLine();
                    for (Account account : customer.accounts) {
                        account.PrintReceipt();
                    }
                    System.out.print("Input Account Number: ");
                    AccountNumber = scanner.nextInt();
                    System.out.print("Input the deposit amount: ");
                    scanner.nextLine();
                    double DepositAmount = scanner.nextDouble();
                    scanner.nextLine();
                    for (Account account : customer.accounts) {
                        if (account.AccountNumber == AccountNumber) {
                            account.Deposit(DepositAmount);
                        }
                    }
                    System.out.println("Account Number not found.");
                    break;

                /*
                 * call Withdraw method with account type
                 */
                case 4:
                    scanner.nextLine();
                    System.out.print("Input Account Number: ");
                    AccountNumber = scanner.nextInt();
                    System.out.print("Input the withdrawal amount: ");
                    scanner.nextLine();
                    double WithdrawalAmount = scanner.nextDouble();
                    for(Account account : customer.accounts){
                        if(account.AccountNumber == AccountNumber){
                            account.Withdraw(WithdrawalAmount);
                        }
                    }
                    System.out.println("Account Number not found.");
                    break;

                /*
                 * Transfer between accounts
                 */
                case 5:
                    scanner.nextLine();
                    break;

                /*
                 * Close a certain account, need account id
                 */
                case 6:
                    scanner.nextLine();
                    break;

                /*
                 * Exit terminal
                 */
                case 7:
                    scanner.nextLine();
                    return;

            }
        }
    }

    public static void seedDatabase(List<Customer> customers) {
        Customer c1 = new Customer("admin", "admin123");
        Customer c2 = new Customer("sample", "sample123");
        customers.add(c1);
        customers.add(c2);
    }

    public interface ITransaction {

        // forces abstraction
        // any class implementing this interface will know how to display transaction
        void PrintReceipt();
    }

    public static class User {
        private String username;
        private String password;

        public User(String username, String password) {
            this.username = username;
            this.password = password;
        }
    }

    public static class Customer extends User {
        public Customer(String username, String password) {
            super(username, password);
        }

        // public and private fields = encapsulation
        private static int CustomerID = 0;
        private String FirstName;
        private String LastName;
        private List<Account> accounts = new ArrayList<Account>();

        public void setName(String firstName, String lastName) {
            this.FirstName = firstName;
            this.LastName = lastName;
        }

        public String getName() {
            return this.FirstName + " " + this.LastName;
        }

        public static Account createAccount(int AccountType, Customer AccountHolder) {
        Account newAccount = null;
        if(AccountType == 1){
            newAccount = new CheckingAccount(AccountHolder, 0);
            AccountHolder.accounts.add(newAccount);
        }
        else if(AccountType == 2){
            newAccount = new SavingsAccount(AccountHolder, 0);
            AccountHolder.accounts.add(newAccount);
        }
        else{
            return null;
        }
        return newAccount;
    }
    }

    public static class Admin extends User {
        int id;

        public Admin(String username, String password) {
            super(username, password);
        }

        List<User> users = new ArrayList<>();
    }

    public static abstract class Account implements ITransaction {
        static int NumberCounter = 0;
        int AccountNumber;
        Customer AccountHolder;
        double balance;

        public Account(Customer AccountHolder, double balance) {
            this.AccountNumber = NumberCounter++;
            this.AccountHolder = AccountHolder;
            this.balance = balance;
        }

        @Override
        public void PrintReceipt() {
            System.out.println("Receipt: Account " + this.AccountNumber + ", balance " + this.balance);
        }

        void Deposit(double amount) {
            this.balance += amount;
        }

        abstract void Withdraw(double amount);
    }

    public static class CheckingAccount extends Account {
        String accountType = "CheckingAccount";
        double OverdraftLimit;

        public CheckingAccount(Customer AccountHolder, double balance) {
            super(AccountHolder, balance);
        }

        @Override
        public void Withdraw(double amount) {
            this.balance -= amount;
        }
    }

    public static class SavingsAccount extends Account {
        String accountType = "SavingAccount";
        double InterestRate;

        public SavingsAccount(Customer AccountHolder, double balance) {
            super(AccountHolder, balance);
        }

        @Override
        public void Withdraw(double amount) {
            double diff = this.balance - amount;
            // 199 - 100
            // 199 - 98
            if (diff <= 100) {
                return;
            } else {
                this.balance -= amount;
            }
        }

    }
}
