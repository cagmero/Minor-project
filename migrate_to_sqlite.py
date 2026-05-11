
import sqlite3
import re
import os

def migrate():
    sql_file = 'quicky.sql'
    db_file = 'test_wise.db'

    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # 1. Strip all /*! ... */ MySQL specific comments first
    sql_content = re.sub(r'/\*!.*?\*/;', '', sql_content, flags=re.DOTALL)
    sql_content = re.sub(r'/\*!.*?\*/', '', sql_content, flags=re.DOTALL)
    
    # 2. Remove other comments
    sql_content = re.sub(r'--.*?\n', '', sql_content)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)

    # 3. Remove MySQL specific commands
    sql_content = re.sub(r'SET .*?;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'LOCK TABLES.*?;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'UNLOCK TABLES;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'ALTER TABLE .*? DISABLE KEYS;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'ALTER TABLE .*? ENABLE KEYS;', '', sql_content, flags=re.IGNORECASE)

    # 4. Clean column definitions
    sql_content = re.sub(r'CHARACTER SET \w+', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'COLLATE \w+', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'COMMENT \'.*?\'', '', sql_content, flags=re.IGNORECASE)

    # 5. Fix AUTO_INCREMENT (must be INTEGER PRIMARY KEY)
    sql_content = re.sub(r'(`\w+`| \w+ ) (INT|INTEGER)(.*?)NOT NULL AUTO_INCREMENT', r'\1 INTEGER PRIMARY KEY AUTOINCREMENT', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'(`\w+`| \w+ ) (INT|INTEGER)(.*?)AUTO_INCREMENT', r'\1 INTEGER PRIMARY KEY AUTOINCREMENT', sql_content, flags=re.IGNORECASE)

    # 6. Fix types
    sql_content = re.sub(r'int\(\d+\)', 'INTEGER', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'double', 'REAL', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'datetime', 'TEXT', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'(?<=\s)date(?=\s|,|\)|;)', 'TEXT', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'timestamp', 'TEXT', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'varchar\(\d+\)', 'TEXT', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'longtext', 'TEXT', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'tinyint\(1\)', 'INTEGER', sql_content, flags=re.IGNORECASE)

    # 7. Fix UNIQUE KEY and other MySQL keys
    sql_content = re.sub(r'USING BTREE', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'UNIQUE KEY `\w+` \((.*?)\)', r'UNIQUE(\1)', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'KEY `\w+` \(`(\w+)`\)', r'', sql_content, flags=re.IGNORECASE) # SQLite doesn't need these explicit keys usually

    # 8. Remove table level options (ENGINE, DEFAULT CHARSET, etc.)
    sql_content = re.sub(r'\) ENGINE=.*?;\s*', r');', sql_content, flags=re.IGNORECASE | re.DOTALL)
    
    # 9. Clean up duplicate Primary Keys in CREATE TABLE
    def clean_create_table(match):
        content = match.group(0)
        # Find if we already have a PRIMARY KEY AUTOINCREMENT
        pk_auto_match = re.search(r'(`\w+`) INTEGER PRIMARY KEY AUTOINCREMENT', content, flags=re.IGNORECASE)
        if pk_auto_match:
            pk_col = pk_auto_match.group(1)
            # Remove standalone PRIMARY KEY for THIS column
            content = re.sub(r',?\s*PRIMARY KEY\s*\(' + re.escape(pk_col) + r'\)', '', content, flags=re.IGNORECASE)
        
        # Remove trailing commas before the closing parenthesis
        content = re.sub(r',\s*\)', r'\n)', content)
        return content

    sql_content = re.sub(r'CREATE TABLE.*?\);', clean_create_table, sql_content, flags=re.DOTALL | re.IGNORECASE)

    # 10. Split and execute
    # Use a more robust split that doesn't break on semicolons inside strings (though unlikely here)
    statements = sql_content.split(';')
    for statement in statements:
        stmt = statement.strip()
        if not stmt or len(stmt) < 10: # Skip junk
            continue
            
        try:
            cursor.execute(stmt)
        except Exception as e:
            print(f"Failed to execute: {stmt[:150]}...\nError: {e}")

    conn.commit()
    conn.close()
    print(f"Successfully migrated {sql_file} to {db_file}")

if __name__ == '__main__':
    migrate()
