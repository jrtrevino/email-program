import pandas as pd


def read_csv(path):
    data_store = None
    try:
        data_store = {}
        # parse data
        dataframe = pd.read_csv(path)
        dataframe['Date'] = pd.to_datetime(dataframe['Date'])
        # Apply formatting lambdas to remove $ symbol
        dataframe['Price'] = dataframe['Price'].apply(
            lambda val: float(val.replace("$", "")))
        dataframe['Tax'] = dataframe['Tax'].apply(
            lambda val: float(val.replace("$", "")))
        dataframe['Shipping'] = dataframe['Shipping'].apply(
            lambda val: float(val.replace("$", "")))
        # add pretax column for tax calculation
        dataframe['Pretax'] = dataframe[[
            'Price', 'Tax', 'Shipping']].sum(axis=1)
        # calculate facebook's tax: 5% or 40 cents minimum
        dataframe['Tax'] = dataframe['Pretax'].apply(
            lambda price: 0.40 if 0.40 > (price*0.05) else (price*0.05))
        # We can calculate the total profit by subtracting Tax from Price
        profit = dataframe['Price'].sum() - dataframe['Tax'].sum()
        # sort transactions by date
        dataframe = dataframe.sort_values(by="Date")
        # update our returning data structure
        data_store['Price'] = dataframe['Price'].sum()
        data_store['Pretax'] = dataframe['Pretax'].sum()
        data_store['Profit'] = profit
        data_store['Tax'] = dataframe['Tax'].sum()
        data_store['Shipping'] = dataframe['Shipping'].sum()
        # place first and last date within the file
        data_store['DateRange'] = [
            str(dataframe['Date'].iloc[0]), str(dataframe['Date'].iloc[-1])]

    except Exception as e:
        print("Error parsing CSV.")
        print(e)

    return data_store


def format_email(data):
    email_txt = f"""
    This is an autogenerated email containing useful information regarding your Facebook transactions.
    This email is triggered nightly if a file is received via email.
    
    Statement period: --- {data['DateRange'][0]} - {data['DateRange'][1]} ---
    
    Total revenue generated: ${data['Price']:.{2}f}
    Total sales tax generated: ${data['Tax']:.{2}f}
    Total shipping charges: ${data['Shipping']:.{2}f}
    Running total (for fee purposes): ${data['Pretax']:.{2}f}
    ---------------------------------------------
    Facebook sales fee: ${data['Tax']:.{2}f}

    Your take home profit: ${data['Profit']:.{2}f}
    """

    print(email_txt)
    return email_txt

def main():
    data = read_csv('../data/test3.csv')
    if data:
        format_email(data)


if __name__ == "__main__":
    main()