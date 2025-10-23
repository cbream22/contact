class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
    def __init__(self, size):
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        """Converts a string key into an array index."""
        hash_sum = 0
        for char in key:
            hash_sum += ord(char)
        return hash_sum % self.size

    def insert(self, key, number):
        """Inserts or updates a contact in the hash table."""
        index = self.hash_function(key)
        new_contact = Contact(key, number)
        new_node = Node(key, new_contact)

        # No collision
        if self.data[index] is None:
            self.data[index] = new_node
            return

        # Collision: Traverse linked list
        current = self.data[index]
        prev = None
        while current:
            if current.key == key:
                # Update existing contact number
                current.value = new_contact
                return
            prev = current
            current = current.next
        prev.next = new_node  # Add new node to end of chain

    def search(self, key):
        """Searches for a contact by name and returns Contact object or None."""
        index = self.hash_function(key)
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self):
        """Prints the current structure of the hash table."""
        for i in range(self.size):
            print(f"Index {i}:", end=" ")
            current = self.data[i]
            if not current:
                print("Empty")
            else:
                while current:
                    print(f"- {current.value}", end=" ")
                    current = current.next
                print()


# --- Testing the HashTable implementation ---
if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()

    print("\nAdding values...\n")
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    table.print_table()

    # Search test
    contact = table.search("John")
    print("\nSearch result:", contact)

    # Collision test
    print("\nTesting collisions...\n")
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")  # May collide
    table.print_table()

    # Duplicate update test
    print("\nTesting duplicate key update...\n")
    table.insert("Rebecca", "999-444-9999")
    table.print_table()

    # Search for non-existent contact
    print("\nSearch result for 'Chris':", table.search("Chris"))


"""
-------------------------------
Design Memo (200–300 words)
-------------------------------

A hash table is ideal for this contact management system because it provides near-constant time performance for insertions, lookups, and updates — usually O(1) on average. When managing hundreds of contacts on a device with limited memory and no database, efficiency is essential. Instead of searching through each contact as in a list, a hash table computes a unique index for each contact’s name, enabling extremely fast access.

This implementation handles collisions using **separate chaining**, meaning that multiple entries that hash to the same index are linked together in a small linked list. If a contact name already exists, the system updates the existing contact rather than adding a duplicate. This ensures both accuracy and memory efficiency while keeping performance stable even when collisions occur.

An engineer might choose a hash table over a list or tree when they prioritize quick, direct access to data rather than maintaining sorted order. Lists are simpler but slower for searches (O(n)), and trees allow ordering but add more complexity and memory overhead. Hash tables offer the best balance between simplicity, speed, and scalability, especially for tasks like name-to-number lookups in contact systems where order is not important but speed is critical.
"""