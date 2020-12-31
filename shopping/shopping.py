import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    print(sys.argv[1])
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    month = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'June':5,'Jul':6,'Aug':7,'Sep':8,'Oct':9,'Nov':10,'Dec':11}
    evidence = []
    label = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        for line in reader:
            #data for evidence
            temp = [cell for cell in line[:17]]

            temp[0] = int(temp[0]) # - Administrative, an integer
            temp[1] = float(temp[1]) # - Administrative_Duration, a floating point number
            temp[2] = int(temp[2]) # - Informational, an integer
            temp[3] = float(temp[3]) # - Informational_Duration, a floating point number
            temp[4] = int(temp[4]) # - ProductRelated, an integer
            temp[5] = float(temp[5]) # - ProductRelated_Duration, a floating point number
            temp[6] = float(temp[6]) # - BounceRates, a floating point number
            temp[7] = float(temp[7]) # - ExitRates, a floating point number
            temp[8] = float(temp[8]) # - PageValues, a floating point number
            temp[9] = float(temp[9]) # - SpecialDay, a floating point number
            temp[10] = month[temp[10]] # - Month, an index from 0 (January) to 11 (December)
            temp[11] = int(temp[11]) # - OperatingSystems, an integer
            temp[12] = int(temp[12]) # - Browser, an integer
            temp[13] = int(temp[13]) # - Region, an integer
            temp[14] = int(temp[14]) # - TrafficType, an integer
            temp[15] = 1 if temp[15]=='Returning_Visitor' else 0 # - VisitorType, an integer 0 (not returning) or 1 (returning)
            temp[16] = 0 if temp[16]=='FALSE' else 1 # - Weekend, an integer 0 (if false) or 1 (if true)
            
            #label
            evidence.append(temp)
            label.append(0 if line[17:][0]=='FALSE' else 1)
    return (evidence, label)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    return model.fit(evidence, labels)




def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0
    for actual, predicted in zip(labels, predictions):
        if(actual == predicted):
            sensitivity += 1
        else:
            specificity += 1
    total = sensitivity+specificity
    return (sensitivity/total, specificity/total)

if __name__ == "__main__":
    main()
