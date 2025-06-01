import csv

def generate_redirect_sql(csv_file_path, output_sql_file, starting_id=18512):
    # SQL template with placeholders
    sql_template = """INSERT INTO `tredirect` (`kRedirect`, `cFromUrl`, `cToUrl`, `nCount`, `cAvailable`, `paramHandling`, `type`, `dateCreated`) VALUES
{values};\n"""

    value_rows = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row_num, row in enumerate(csv_reader, starting_id):
            # Convert cFromUrl to lowercase and handle escaping
            cFromUrl = row.get('cFromUrl', '').strip().lower().replace("'", "''")
            cToUrl = row.get('cToUrl', '').strip().replace("'", "''")

            if not cFromUrl or not cToUrl:
                print(f"Warning: Skipping row - missing URL data")
                continue

            # Preserving all template values exactly
            value_row = (
                f"({row_num}, '{cFromUrl}', '{cToUrl}', "
                "1, 'n', 1, 0, '2025-05-24 08:41:03')"
            )
            value_rows.append(value_row)

    # Write to SQL file in batches of 1000
    with open(output_sql_file, 'w', encoding='utf-8') as sql_file:
        for i in range(0, len(value_rows), 1000):
            batch = value_rows[i:i + 1000]
            values_clause = ",\n".join(batch)
            sql_file.write(sql_template.format(values=values_clause))

    print(f"SQL file generated successfully at {output_sql_file}")
    print(f"First kRedirect value: {starting_id}")
    print(f"Last kRedirect value: {starting_id + len(value_rows) - 1}")

# Example usage
if __name__ == '__main__':
    generate_redirect_sql(
        csv_file_path='red.csv',
        output_sql_file='redirect_inserts.sql',
        starting_id=18512  # Now starting from 9642 as requested
    )
