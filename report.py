import os
import json
import xmltodict
import re
import mariadb
import pandas as pd
import matplotlib.pyplot as plt
import weasyprint

def main():
    cur = db().cur
    conn = db().conn
    cur.execute("SELECT * FROM score WHERE scope IS NOT NULL")
    rows = cur.fetchall()

# create a dataframe
    df = pd.DataFrame(rows, columns=['Name', 'Total', 'Pass', 'Percentage', 'Checked by'])
    color_map = {'APP': 'red', 'CON': 'blue', 'NET': 'green'}
    df['Description'] = ''
    df['Color'] = df['Name'].apply(lambda x: color_map[x[:3]])

    # create a pie chart
    plt.figure(figsize=(10, 10))
    for i, row in df.iterrows():
        cur.execute("SELECT * FROM Data WHERE ID = ?", (row['Name'],))
        description = cur.fetchone()
        df.at[i, 'Description'] = description[3]
        plt.bar(row['Name'], row['Percentage']*100, color=row['Color'])
    plt.xticks(rotation=270)
    plt.savefig('bar_chart.png')

    # create an HTML report
    with open('report.html', 'w') as f:
        f.write('<html><head><title>Report</title><link rel="stylesheet" href="style.css"></head><style></style><body style="width:700px;margin:auto;">')
        f.write('<h1 style="text-align:center;">Report</h1>')
        f.write(df.to_html(index=False, columns=['Name', 'Total', 'Pass', 'Percentage', 'Description']))
        f.write('<br><img style="width:700px;" src="bar_chart.png" alt="Bar Chart">')
        f.write('</body></html>')
        f.close()
    weasyprint.HTML(filename='report.html').write_pdf('report.pdf')
























class database:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="root",
                host="localhost",
                port=3306,
                database="eits"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()


def db():
    return database()

if __name__ == "__main__":
    main()