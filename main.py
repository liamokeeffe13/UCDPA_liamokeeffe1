import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np


def is_customer_streaming(cu_id, customer_by_streaming_movies_dict, customer_by_streaming_tv_dict):
    return customer_by_streaming_movies_dict[cu_id] == "Yes" or customer_by_streaming_tv_dict[cu_id] == "Yes"


if __name__ == '__main__':


    #  2. Generate the CSV - Pandas DataFrame
    data = pd.read_csv(r'C:\Users\lokeeffe\Downloads\CustomerChurn.csv')

    customer_ids = list(data.customerID)
    customer_genders = list(data.gender)

    female_count = len([f for f in customer_genders if f == "Female"])
    male_count = len([m for m in customer_genders if m == "Male"])

    customer_ids_to_gender = dict(zip(customer_ids, customer_genders))
    # 4. Drop duplicates -
    print(f"Number of customer ids before deduping {len(customer_ids)}")

    customer_ids_deduped = set(customer_ids)

    print(f"Number of customer ids before deduping {len(customer_ids_deduped)}")

    # Gender distribution
    plt.bar(["Female", "Male"], [female_count, male_count])
    plt.title("Gender Distribution")
    plt.xlabel("Gender")
    plt.ylabel("Customers")
    plt.show()
    
    corrMatrix = data.corr()
    sns.heatmap(corrMatrix, annot=True)
    plt.show()

    # The tenure as it relates to churn -
    churn = data.Churn
    tenure = data.tenure
    customer_id = data.customerID
    customer_payment_methods = data.PaymentMethod
    customer_with_dependents = data.Dependents
    customer_with_streaming_movies = data.StreamingMovies
    customer_with_streaming_tv = data.StreamingTV

    customer_by_tenure = dict(zip(customer_id, tenure))
    customer_by_churn = dict(zip(customer_id, churn))
    customer_by_payment_method = dict(zip(customer_id, customer_payment_methods))

    customer_churn_and_tenure = {
        customer_id: {
            "churn": customer_by_churn[customer_id],
            "tenure": customer_by_tenure[customer_id]
        } for customer_id in customer_by_tenure.keys()}

    no_churn = []
    yes_churn = []

    for k, v in customer_churn_and_tenure.items():
        if v["churn"] == "No":
            no_churn.append(v["tenure"])
        elif v["churn"] == "Yes":
            yes_churn.append(v["tenure"])

    avg_per_no_churn = sum(no_churn ) /len(no_churn)
    avg_per_yes_churn = sum(yes_churn ) /len(yes_churn)

    # Churn distribution
    plt.bar(["Yes", "No"], [avg_per_yes_churn, avg_per_no_churn], color="green")
    plt.title("Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Avg Tenure (Years)")
    plt.show()

    # Pie chart of Payment methods

    ax = (data['PaymentMethod'].value_counts() * 100.0 / len(data)) \
        .plot.pie(autopct='%.1f%%', figsize=(10, 10), fontsize=14)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_axis_off()
    ax.set_title('% of Payment methods', fontsize=12)

    plt.show()


    # Distribution of customers_with_dependents_who_use_streaming_services

    customer_by_dependents = dict(zip(customer_id, customer_with_dependents))
    customer_by_streaming_movies = dict(zip(customer_id, customer_with_streaming_movies))
    customer_by_streaming_tv = dict(zip(customer_id, customer_with_streaming_tv))

    customers_with_dependents_who_stream = 0
    customers_without_dependents_who_stream = 0
    customers_with_dependents_who_dont_stream = 0
    customers_without_dependents_who_dont_stream = 0

    for k, v in customer_by_dependents.items():
        if is_customer_streaming(k, customer_by_streaming_movies, customer_by_streaming_tv):
            if v == "Yes":
                customers_with_dependents_who_stream += 1
            else:
                customers_without_dependents_who_stream += 1
        else:
            if v == "Yes":
                customers_with_dependents_who_dont_stream += 1
            else:
                customers_without_dependents_who_dont_stream += 1

    plt.pie([customers_with_dependents_who_stream,
             customers_with_dependents_who_dont_stream,
             customers_without_dependents_who_stream,
             customers_without_dependents_who_dont_stream], labels=[
        'With dependents who stream',
        'With dependents who dont stream',
        'Without dependents who stream',
        'Without dependents who dont stream'
    ], autopct='%.1f%%', textprops={'fontsize': 6})
    # month_cor.plot.scatter(x='MonthlyCharges', y='TotalCharges', figsize=(20, 20))
    plt.show()


    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(20, 6))

    ax = sns.distplot(data[data['PhoneService'] == 'No'][data["InternetService"] != "No"]['tenure'],
                      hist=True, kde=False,
                      bins=int(180 / 5), color='turquoise',
                      hist_kws={'edgecolor': 'black'},
                      kde_kws={'linewidth': 4},
                      ax=ax1)
    ax.set_ylabel('# of Customers')
    ax.set_xlabel('Tenure (months)')
    ax.set_title('No Phone Service but Internet')

    ax = sns.distplot(data[data['PhoneService'] == 'Yes'][data["InternetService"] != "No"]['tenure'],
                      hist=True, kde=False,
                      bins=int(180 / 5), color='turquoise',
                      hist_kws={'edgecolor': 'black'},
                      kde_kws={'linewidth': 4},
                      ax=ax2)
    ax.set_ylabel('# of Customers')
    ax.set_xlabel('Tenure (months)')
    ax.set_title('Phone Service and Internet')

    plt.show()
    print("Done")

    

    
    
    
    
   
    

