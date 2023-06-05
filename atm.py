from datetime import datetime

""" Accounts Handling """

# Define constant name
ACCOUNTNAME = 'name'
PINNUMBER = 'pin'

class Accounts:
    """ Class to maintain the account list """

    # Static variables
    filename = "accounts.csv"
    members = {}

    def __init__(self):
        self.accountid = ""
        # initialize account detailes for first time object creation
        if len(Accounts.members) == 0:
            self.loadAccounts()

    def loadAccounts(self):
        print
        print "loading accounts details in members dictionary"
        Accounts.members.clear()

        # open the file
        with open(Accounts.filename,"r") as f:
            # read and load the dictionary
            lines = f.readlines()

        for line in lines:
            if len(line.strip()) > 0:
                fields = line.split(",")
                accountid = fields[0].strip()
                accountname = fields[1].strip()
                pinnumber = fields[2].strip()

                Accounts.members[accountid] = {ACCOUNTNAME: accountname, PINNUMBER: pinnumber}


    def validateAccountid(self, accountid):
        # validate this is available in dictionary
        if Accounts.members.has_key(accountid):
            self.accountid = accountid
            return Accounts.members[accountid][ACCOUNTNAME]
        else:
            raise Exception("Invalid account number.")

    def validatePinnumber(self, pinnumber):
        # validate this is available in dictionary
        if Accounts.members.has_key(self.accountid):
            pin = Accounts.members[self.accountid][PINNUMBER]
            return (pin == pinnumber)
        else:
            raise Exception("Invalid pin number.")



""" Transactions handling """

class Transactions:
    """This class maintain deposit, withdraw, list datas"""
    filename = "transactions.csv"

    def deposit(self, accountid, amount):
        # write the transaction in file
        with open(Transactions.filename, "a") as f:
            trandate = datetime.now().strftime("%d/%m/%y %X")
            f.write("{an}, {dt}, Deposit, {amt}\n" .format(an=accountid, dt=trandate, amt=amount))

    def withdraw(self, accountid, amount):
        # write the transaction in file
        with open(Transactions.filename, "r") as f:
            #for getting Closing balance
            closingBalance = 0
            trans = []
            for line in f.readlines():
                fields = line.split(",")
                if fields[0] == accountid:
                    trans.append(line.strip())


            for tran in trans:
                fields = tran.split(",")
                trantype = fields[2].strip()
                amt = float(fields[3])
                if trantype == "Withdraw":
                    amt = -amt
                closingBalance += amt

            if amount > closingBalance:
                print "Insufficient amount Requested! Please Enter to continue..."
            else:
                with open(Transactions.filename, "a") as f:
                    trandate = datetime.now().strftime("%d/%m/%y %X")
                    f.write("{an}, {dt}, Withdraw, {amt}\n".format(an=accountid, dt=trandate, amt=amount))
                    print "Withdraw successfully completed. Please Enter to continue..."

    def listTransactions(self, accountid):
        #opening file
        with open(Transactions.filename, "r") as f:
            trans = []
            for line in f.readlines():
                fields = line.split(",")
                if fields[0]==accountid:
                    trans.append(line.strip())
        # display records
        print "Transactions"
        print "--------------"
        closingBalance = 0
        for tran in trans:
            fields = tran.split(",")
            trandate = fields[1].strip()
            trantype = fields[2].strip()
            amount = float(fields[3])
            if trantype == "Withdraw":
                amount = -amount
            closingBalance += amount
            print "{} {:<20s} {:10.2f}" .format(trandate, trantype,amount)
        print
        print "Closing Balance : %.2f" %closingBalance
        print


""" menu handling """

class ATMMenu:
    """ Integration of accounts and transactions """

    def __init__(self):
        self.acts = Accounts()
        self.txn = Transactions()

    def start(self):
        while True:
            print "Tamilnadu Bank Limited."
            print
            ano = raw_input("Enter account number : ")
            #Verify the account number
            try:
                accountname = self.acts.validateAccountid(ano)
                print "Welcome %s" %accountname
            except Exception as e:
                print "Invalid account number! Please enter to continue"
                x = raw_input()
                continue

            # verify the pin number
            pin = raw_input("Enter pin number : ")
            if self.acts.validatePinnumber(pin) == False:
                print "Invalid Pin number! Please enter to continue"
                x = raw_input()
                continue
            self.transactionMenu()

    def transactionMenu(self):
        while True:
            print "Your Option"
            print
            print "1. Deposit Money"
            print "2. Withdraw Money"
            print "3. List Transactions"
            print "4. Exit"
            print
            opt = input("Enter Option (1-4) : ")

            if opt == 4:
                break
            elif opt == 1:
                amount = input("Enter deposit Amount : ")
                self.txn.deposit(self.acts.accountid, amount)
                print "Deposit successfully completed. Please Enter to continue"
                x = raw_input()
                continue
            elif opt == 2:
                amount = input("Enter Withdraw Amount : ")
                self.txn.withdraw(self.acts.accountid, amount)
                x = raw_input()
                continue
            elif opt == 3:
                self.txn.listTransactions(self.acts.accountid)
            else:
                print "Invalid option. Try again. Press Enter to continue."
                x = raw_input()


""" main handling """

menu = ATMMenu()
menu.start()