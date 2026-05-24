from models import db, Category, Question

def seed_database():
    print("Seeding database...")
    
    # 1. Add Categories
    categories_data = [
        {
            "name": "Python Programming",
            "description": "Test your knowledge of Python syntax, data types, object-oriented concepts, and advanced features.",
            "icon": "code"
        },
        {
            "name": "Data Structures",
            "description": "Challenge yourself with questions on arrays, stacks, queues, linked lists, trees, and algorithmic complexity.",
            "icon": "layers"
        },
        {
            "name": "Web Development",
            "description": "HTML, CSS, flexbox layouts, semantic markup, and browser behaviors.",
            "icon": "globe"
        },
        {
            "name": "Database Systems",
            "description": "SQL queries, joins, foreign keys, ACID transactions, and MySQL features.",
            "icon": "database"
        }
    ]
    
    categories = {}
    for cat_info in categories_data:
        existing = Category.query.filter_by(name=cat_info["name"]).first()
        if not existing:
            cat = Category(
                name=cat_info["name"],
                description=cat_info["description"],
                icon=cat_info["icon"]
            )
            db.session.add(cat)
            db.session.commit()
            categories[cat.name] = cat
            print(f"Added category: {cat.name}")
        else:
            categories[existing.name] = existing
            print(f"Category already exists: {existing.name}")

    # 2. Add Questions
    questions_data = [
        # --- PYTHON PROGRAMMING ---
        {
            "category": "Python Programming",
            "difficulty": "Easy",
            "question_text": "What is the output of print(2 ** 3) in Python?",
            "option_a": "6",
            "option_b": "8",
            "option_c": "9",
            "option_d": "5",
            "correct_answer": "B",
            "explanation": "The ** operator in Python represents exponentiation (power). Thus, 2 ** 3 represents 2 raised to the power of 3, which is 2 * 2 * 2 = 8."
        },
        {
            "category": "Python Programming",
            "difficulty": "Easy",
            "question_text": "Which of the following is an immutable data type in Python?",
            "option_a": "List",
            "option_b": "Dictionary",
            "option_c": "Tuple",
            "option_d": "Set",
            "correct_answer": "C",
            "explanation": "A Tuple is immutable, meaning its elements cannot be altered, added, or deleted once created. Lists, Dictionaries, and Sets are mutable."
        },
        {
            "category": "Python Programming",
            "difficulty": "Medium",
            "question_text": "What does the __init__ method do in a Python class?",
            "option_a": "It deletes an instance of the class.",
            "option_b": "It initializes a class class-level variable.",
            "option_c": "It acts as a constructor to initialize a newly created object's state.",
            "option_d": "It imports the module defining the class.",
            "correct_answer": "C",
            "explanation": "The __init__ method is a special method (dunder method) in Python classes that acts as a constructor. It runs automatically when a new instance of the class is created, allowing you to set up initial attributes."
        },
        {
            "category": "Python Programming",
            "difficulty": "Medium",
            "question_text": "Which list comprehension correctly filters even numbers from range(10)?",
            "option_a": "[x if x % 2 == 0 for x in range(10)]",
            "option_b": "[x for x in range(10) if x % 2 == 0]",
            "option_c": "[x for x % 2 == 0 in range(10)]",
            "option_d": "[if x % 2 == 0: x for x in range(10)]",
            "correct_answer": "B",
            "explanation": "The standard syntax for a list comprehension with a simple filter is [expression for item in iterable if condition]. Therefore, [x for x in range(10) if x % 2 == 0] is correct."
        },
        {
            "category": "Python Programming",
            "difficulty": "Hard",
            "question_text": "What is a generator in Python, and how is it defined?",
            "option_a": "A generator is a module that creates random numbers, defined using the random keyword.",
            "option_b": "A generator is a function that returns an iterator using the 'yield' keyword to produce values lazily.",
            "option_c": "A generator is a system-level process that runs Python scripts concurrently.",
            "option_d": "A generator is another name for a lambda function.",
            "correct_answer": "B",
            "explanation": "Generators are functions that return an iterator object, yielding items one at a time on demand. They are defined like normal functions but use the 'yield' keyword instead of 'return' to preserve state between calls, conserving memory."
        },
        {
            "category": "Python Programming",
            "difficulty": "Hard",
            "question_text": "What is the purpose of 'self' in Python class methods?",
            "option_a": "It is a keyword that refers to the class itself, similar to 'cls'.",
            "option_b": "It refers to the current instance of the class, allowing access to instance attributes and methods.",
            "option_c": "It is a security mechanism that prevents private variable modification.",
            "option_d": "It calls the parent class constructor.",
            "correct_answer": "B",
            "explanation": "By convention, 'self' is the first parameter of any instance method in a Python class. It refers to the specific object instance that called the method, enabling access to instance-specific attributes and other methods."
        },

        # --- DATA STRUCTURES ---
        {
            "category": "Data Structures",
            "difficulty": "Easy",
            "question_text": "What is the time complexity of accessing an element in an array by its index?",
            "option_a": "O(N)",
            "option_b": "O(log N)",
            "option_c": "O(1)",
            "option_d": "O(N log N)",
            "correct_answer": "C",
            "explanation": "Since array elements are stored in contiguous memory locations, the address of any element can be computed in constant time using its index and the base address. Therefore, the access time complexity is O(1)."
        },
        {
            "category": "Data Structures",
            "difficulty": "Easy",
            "question_text": "Which data structure operates on a Last-In-First-Out (LIFO) basis?",
            "option_a": "Queue",
            "option_b": "Stack",
            "option_c": "Linked List",
            "option_d": "Binary Tree",
            "correct_answer": "B",
            "explanation": "A Stack operates on a Last-In-First-Out (LIFO) principle, where the last element added is the first one to be removed. In contrast, a Queue operates on a First-In-First-Out (FIFO) basis."
        },
        {
            "category": "Data Structures",
            "difficulty": "Medium",
            "question_text": "In a Binary Search Tree (BST), what is the worst-case time complexity for searching an element?",
            "option_a": "O(1)",
            "option_b": "O(log N)",
            "option_c": "O(N)",
            "option_d": "O(N log N)",
            "correct_answer": "C",
            "explanation": "In the worst case (when the tree is skewed or degenerate, behaving like a linked list), you may have to traverse all N nodes. The worst-case search complexity is O(N). In a balanced BST, the search complexity is O(log N)."
        },
        {
            "category": "Data Structures",
            "difficulty": "Medium",
            "question_text": "Which data structure is typically used to implement Breadth-First Search (BFS) in a graph?",
            "option_a": "Stack",
            "option_b": "Queue",
            "option_c": "Min-Heap",
            "option_d": "Hash Table",
            "correct_answer": "B",
            "explanation": "BFS explores nodes level-by-level. A Queue is used to store and process vertices in FIFO order, ensuring that nodes closer to the starting node are visited before those further away. DFS (Depth-First Search) typically uses a Stack."
        },
        {
            "category": "Data Structures",
            "difficulty": "Hard",
            "question_text": "What is a hash collision in a Hash Table?",
            "option_a": "When the hash function fails to compute a value and throws an exception.",
            "option_b": "When two distinct keys produce the same hash value, mapping them to the same index.",
            "option_c": "When the table runs out of memory and crashes.",
            "option_d": "When keys are deleted, leaving empty memory slots.",
            "correct_answer": "B",
            "explanation": "A hash collision occurs when two different keys produce the same integer index after being processed by a hash function. Collision resolution techniques include Chaining (linked lists at each slot) and Open Addressing (probing)."
        },
        {
            "category": "Data Structures",
            "difficulty": "Hard",
            "question_text": "What is a balanced binary tree, and why is it important?",
            "option_a": "A tree where all leaves have the same value, which makes tree traversals trivial.",
            "option_b": "A tree where the heights of the left and right subtrees of any node differ by at most one, ensuring logarithmic operations.",
            "option_c": "A tree where every node has exactly zero or two children.",
            "option_d": "A tree with no empty nodes, which saves memory.",
            "correct_answer": "B",
            "explanation": "A balanced binary tree (e.g., AVL tree, Red-Black tree) keeps its height at O(log N). This is important because the time complexity of operations like search, insertion, and deletion depend on height. Balancing guarantees O(log N) worst-case performance."
        },

        # --- WEB DEVELOPMENT ---
        {
            "category": "Web Development",
            "difficulty": "Easy",
            "question_text": "What does HTML stand for?",
            "option_a": "HyperText Markup Language",
            "option_b": "HighText Machine Language",
            "option_c": "HyperTransfer Markup Layout",
            "option_d": "HyperLink and Text Markup Language",
            "correct_answer": "A",
            "explanation": "HTML stands for HyperText Markup Language. It is the standard markup language used to structure documents and pages for display in a web browser."
        },
        {
            "category": "Web Development",
            "difficulty": "Easy",
            "question_text": "Which CSS property is used to change the text color of an element?",
            "option_a": "background-color",
            "option_b": "font-color",
            "option_c": "text-color",
            "option_d": "color",
            "correct_answer": "D",
            "explanation": "In CSS, the 'color' property is used to specify the text color of an element. The 'background-color' property sets the background color of the element."
        },
        {
            "category": "Web Development",
            "difficulty": "Medium",
            "question_text": "What is the difference between 'display: none' and 'visibility: hidden' in CSS?",
            "option_a": "'display: none' keeps the space in the layout, while 'visibility: hidden' removes it.",
            "option_b": "'display: none' removes the element from the layout flow, whereas 'visibility: hidden' hides the element but keeps its space in the layout.",
            "option_c": "There is no difference; they are aliases for the same visual behavior.",
            "option_d": "'display: none' only works on block elements; 'visibility: hidden' only works on inline elements.",
            "correct_answer": "B",
            "explanation": "'display: none' renders nothing and removes the element completely from the document flow (other elements collapse into its space). 'visibility: hidden' makes the element invisible, but it still takes up its original space and affects layout positioning."
        },
        {
            "category": "Web Development",
            "difficulty": "Medium",
            "question_text": "What does the 'box-sizing: border-box' CSS rule do?",
            "option_a": "It hides the borders of an element.",
            "option_b": "It includes padding and border in the element's total declared width and height.",
            "option_c": "It forces borders to remain inside circular elements.",
            "option_d": "It excludes padding and borders, making elements wider than their specified width.",
            "correct_answer": "B",
            "explanation": "By default, browsers calculate size as 'content-box' (width/height + padding + border). 'border-box' tells the browser to include padding and border within the specified width and height, which makes sizing grid structures much easier."
        },
        {
            "category": "Web Development",
            "difficulty": "Hard",
            "question_text": "What is the purpose of the 'defer' attribute in an HTML <script> tag?",
            "option_a": "It prevents the script from executing until the user clicks on the page.",
            "option_b": "It downloads the script asynchronously and executes it immediately, blocking document parsing.",
            "option_c": "It downloads the script in parallel and executes it only after the HTML document has been fully parsed.",
            "option_d": "It compiles the JavaScript code using a WebAssembly compiler.",
            "correct_answer": "C",
            "explanation": "The 'defer' attribute specifies that the script is executed after the document parsing is complete. The script is downloaded in parallel (asynchronously), but execution is deferred, and deferred scripts execute in the order they appear in the document."
        },
        {
            "category": "Web Development",
            "difficulty": "Hard",
            "question_text": "In CSS Flexbox, what does the 'flex-grow' property define?",
            "option_a": "It specifies how much a flex item will grow relative to the rest of the flex items when positive free space is available.",
            "option_b": "It sets the maximum physical height of a flex container.",
            "option_c": "It forces elements to wrap onto multiple lines when they run out of space.",
            "option_d": "It scales up fonts within a flex item when the browser zooms in.",
            "correct_answer": "A",
            "explanation": "'flex-grow' defines the ability of a flex item to grow if necessary. It accepts a unitless value that serves as a proportion, detailing how much of the remaining space in the flex container the item should take up relative to others."
        },

        # --- DATABASE SYSTEMS ---
        {
            "category": "Database Systems",
            "difficulty": "Easy",
            "question_text": "What does SQL stand for?",
            "option_a": "Simple Query Language",
            "option_b": "Structured Query Language",
            "option_c": "System Query Logic",
            "option_d": "Server Query Layout",
            "correct_answer": "B",
            "explanation": "SQL stands for Structured Query Language. It is the standard language designed for managing data held in relational database management systems (RDBMS) like MySQL, PostgreSQL, SQLite, etc."
        },
        {
            "category": "Database Systems",
            "difficulty": "Easy",
            "question_text": "Which SQL clause is used to filter records based on a specific condition?",
            "option_a": "GROUP BY",
            "option_b": "ORDER BY",
            "option_c": "WHERE",
            "option_d": "HAVING",
            "correct_answer": "C",
            "explanation": "The WHERE clause is used to filter records in SQL, extracting only those records that satisfy a specified condition. HAVING is used to filter groups created by GROUP BY."
        },
        {
            "category": "Database Systems",
            "difficulty": "Medium",
            "question_text": "What is a Foreign Key in a database schema?",
            "option_a": "A key that is encrypted for remote security access.",
            "option_b": "A field in one table that uniquely identifies a row of another table, linking the two tables together.",
            "option_c": "A column that cannot contain null values.",
            "option_d": "A key that allows access from third-party client applications.",
            "correct_answer": "B",
            "explanation": "A Foreign Key is a column (or group of columns) in a relational database table that provides a link between data in two tables. It references the Primary Key of another table, enforcing referential integrity."
        },
        {
            "category": "Database Systems",
            "difficulty": "Medium",
            "question_text": "What is the difference between an INNER JOIN and a LEFT JOIN in SQL?",
            "option_a": "INNER JOIN returns all rows from both tables; LEFT JOIN only returns matching rows.",
            "option_b": "INNER JOIN returns rows that have matching values in both tables; LEFT JOIN returns all rows from the left table, and the matched rows from the right table.",
            "option_c": "INNER JOIN is faster but loses database records; LEFT JOIN is slower and preserves historical logs.",
            "option_d": "LEFT JOIN is only used for numerical values; INNER JOIN is for text values.",
            "correct_answer": "B",
            "explanation": "An INNER JOIN selects records that have matching values in both tables. A LEFT (OUTER) JOIN selects all records from the left table, and the matched records from the right table. If there is no match, NULL values are returned for columns of the right table."
        },
        {
            "category": "Database Systems",
            "difficulty": "Hard",
            "question_text": "In Database Systems, what do the ACID properties represent in transactions?",
            "option_a": "Atomicity, Consistency, Isolation, Durability",
            "option_b": "Algorithm, Concurrency, Indexing, Distribution",
            "option_c": "Accuracy, Completeness, Integrity, Dependability",
            "option_d": "Access, Control, Identity, Defense",
            "correct_answer": "A",
            "explanation": "ACID stands for Atomicity (all-or-nothing), Consistency (integrity constraints maintained), Isolation (independent concurrent executions), and Durability (committed changes are permanent). These properties guarantee that database transactions are processed reliably."
        },
        {
            "category": "Database Systems",
            "difficulty": "Hard",
            "question_text": "What is the primary goal of Database Normalization?",
            "option_a": "To index data to make search operations run in constant time O(1).",
            "option_b": "To eliminate data redundancy, prevent insertion/update/deletion anomalies, and organize relationships to protect data integrity.",
            "option_c": "To convert tables into standard JSON documents for modern NoSQL integrations.",
            "option_d": "To backup database contents automatically every hour.",
            "correct_answer": "B",
            "explanation": "Database Normalization is the process of structuring a relational database in accordance with a series of normal forms (1NF, 2NF, 3NF, etc.) to minimize data redundancy, prevent update anomalies, and ensure dependencies make logical sense."
        }
    ]
    
    added_count = 0
    for q_info in questions_data:
        cat = categories.get(q_info["category"])
        if not cat:
            print(f"Skipping question, category not found: {q_info['category']}")
            continue
            
        # Check if question text already exists in category
        existing_q = Question.query.filter_by(
            category_id=cat.id, 
            question_text=q_info["question_text"]
        ).first()
        
        if not existing_q:
            q = Question(
                category_id=cat.id,
                question_text=q_info["question_text"],
                option_a=q_info["option_a"],
                option_b=q_info["option_b"],
                option_c=q_info["option_c"],
                option_d=q_info["option_d"],
                correct_answer=q_info["correct_answer"],
                explanation=q_info["explanation"],
                difficulty=q_info["difficulty"]
            )
            db.session.add(q)
            added_count += 1
        else:
            # Optionally update fields if they changed
            pass

    db.session.commit()
    print(f"Successfully seeded {added_count} new questions!")
