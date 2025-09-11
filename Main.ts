function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

enum PaymentMethod {
  CASH = "cash",
  CARD = "card",
  WALLET = "wallet",
}

class Dish {
  constructor(
    public name: string,
    public price: number,
    public ingredients: string[]
  ) {}
}

class Menu {
  dishes: Dish[] = [
    new Dish("Chicken with rice", 25, ["chicken", "rice"]),
    new Dish("Fresh salad", 18, ["lettuce", "tomato", "cheese"]),
    new Dish("Cheese sandwich", 15, ["bread", "cheese", "tomato"]),
  ];

  showMenu() {
    console.log("\n📖 Available Menu:");
    this.dishes.forEach((d, i) =>
      console.log(`${i + 1}. ${d.name} - $${d.price}`)
    );
  }
}

class Inventory {
  private stock: Record<string, number> = {
    rice: 10,
    chicken: 5,
    lettuce: 8,
    tomato: 6,
    cheese: 4,
    bread: 10,
  };

  check(ingredients: string[]): boolean {
    return ingredients.every((ing) => (this.stock[ing] ?? 0) > 0);
  }

  consume(ingredients: string[]) {
    ingredients.forEach((ing) => {
      this.stock[ing] = (this.stock[ing] ?? 0) - 1;
    });
  }

  showStock() {
    console.log("📦 Current Stock:", this.stock);
  }
}

class Customer {
  history: Dish[] = [];
  constructor(public name: string) {}

  choose(menu: Menu): Dish {
    menu.showMenu();
    const option = parseInt(prompt("👉 Choose a dish (1-3):") || "1");
    const dish = menu.dishes[option - 1] || menu.dishes[0];
    console.log(`${this.name} chose: ${dish.name}`);
    this.history.push(dish);
    return dish;
  }

  askForBill() {
    console.log(`${this.name} asks for the bill 💳`);
  }

  async pay(total: number) {
    const option = prompt(
      "👉 Payment method (cash/card/wallet):"
    )?.toLowerCase();

    const method =
      option === "cash"
        ? PaymentMethod.CASH
        : option === "wallet"
        ? PaymentMethod.WALLET
        : PaymentMethod.CARD;

    console.log(`${this.name} is paying $${total} with ${method}...`);
    await delay(300);
    console.log(`✅ Payment completed by ${this.name}`);
  }
}

class Waiter {
  takeOrder(dish: Dish) {
    console.log(`Waiter takes ${dish.name} to the kitchen 🚶‍♂️`);
  }

  async serve(dish: Dish, customer: Customer) {
    await delay(200);
    console.log(`🍽️ Waiter serves ${dish.name} to ${customer.name}`);
  }
}

class Chef {
  constructor(private inventory: Inventory) {}

  async prepare(dish: Dish): Promise<Dish> {
    if (!this.inventory.check(dish.ingredients)) {
      throw new Error(`❌ Not enough ingredients for ${dish.name}`);
    }
    console.log(`👨‍🍳 Chef is preparing ${dish.name}...`);
    await delay(500);
    this.inventory.consume(dish.ingredients);
    console.log(`✅ ${dish.name} is ready!`);
    return dish;
  }
}

class Cashier {
  history: number[] = [];

  calculate(dishes: Dish[]): number {
    const total = dishes.reduce((s, d) => s + d.price, 0);
    console.log(`💲 Total amount: $${total}`);
    return total;
  }

  issueReceipt(total: number) {
    console.log(`🧾 Receipt issued for $${total}`);
    this.history.push(total);
  }
}

class Manager {
  report(cashier: Cashier) {
    const sales = cashier.history.length;
    const total = cashier.history.reduce((a, b) => a + b, 0);
    console.log(`\n📊 Report: ${sales} sales | Revenue: $${total}`);
  }
}

// Main Flow 
async function restaurantFlow() {
  const menu = new Menu();
  const inventory = new Inventory();
  const chef = new Chef(inventory);
  const waiter = new Waiter();
  const cashier = new Cashier();
  const manager = new Manager();

  const customerName = prompt("👤 Enter your name:") || "Customer";
  const customer = new Customer(customerName);

  const dish = customer.choose(menu);
  waiter.takeOrder(dish);

  try {
    const prepared = await chef.prepare(dish);
    await waiter.serve(prepared, customer);

    customer.askForBill();
    const total = cashier.calculate(customer.history);
    cashier.issueReceipt(total);
    await customer.pay(total);

  } catch (err: any) {
    console.log("⚠️ Order error:", err.message);
  }

  inventory.showStock();
  manager.report(cashier);
}

// Run
restaurantFlow();

