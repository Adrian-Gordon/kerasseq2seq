from matplotlib import pyplot as plt

def plot_prediction(x, y_true, y_pred):
    """Plots the predictions.
    
    Arguments
    ---------
    x: Input sequence of shape (input_sequence_length,
        dimension_of_signal)
    y_true: True output sequence of shape (input_sequence_length,
        dimension_of_signal)
    y_pred: Predicted output sequence (input_sequence_length,
        dimension_of_signal)
    """

    plt.figure(figsize=(12, 3))

    output_dim = y_true.shape[-1]
    for j in range(output_dim):
        past = x[:, j] 
        true = y_true[:, j]
        pred = y_pred[:, j]

        label1 = "Seen (past) values" if j==0 else "_nolegend_"
        label2 = "True future values" if j==0 else "_nolegend_"
        label3 = "Predictions" if j==0 else "_nolegend_"

        plt.plot(range(len(past)), past, "o--b",
                 label=label1)
        plt.plot(range(len(past),
                 len(true)+len(past)), true, "x--b", label=label2)
        plt.plot(range(len(past), len(pred)+len(past)), pred, "o--y",
                 label=label3)
    plt.legend(loc='best')
    plt.title("Predictions v.s. true values")
    plt.show()



def plot_price_prediction(x, y_true, y_pred):
    """Plots the predictions.
    
    Arguments
    ---------
    x: Input sequence of shape (input_sequence_length,
        dimension_of_signal)
    y_true: True output sequence of shape (input_sequence_length,
        dimension_of_signal)
    y_pred: Predicted output sequence (input_sequence_length,
        dimension_of_signal)
    """

    plt.figure(figsize=(12, 3))
    
    pastLayprice = x[:,0]
    label1 = "observed layprice"
    plt.plot(range(len(pastLayprice)), pastLayprice, "--b",label=label1)
    
    pastBackprice = x[:,2]
    label1 = "observed backprice"
    plt.plot(range(len(pastBackprice)), pastBackprice, "--g",label=label1)

    trueLayprice = y_true[:,0]
    plt.plot(range(len(pastLayprice),len(trueLayprice)+len(pastLayprice)),trueLayprice,"--b")
    
    trueBackprice = y_true[:,1]
    plt.plot(range(len(pastBackprice),len(trueBackprice)+len(pastBackprice)),trueBackprice,"--g")

    label1="predicted layprice"
    predictedLayprice = y_pred[:,0]
    plt.plot(range(len(pastLayprice), len(predictedLayprice)+len(pastLayprice)), predictedLayprice, "o--b", label=label1)
    
    label1="predicted backprice"
    predictedBackprice = y_pred[:,1]
    plt.plot(range(len(pastBackprice), len(predictedBackprice)+len(pastBackprice)), predictedBackprice, "o--g", label=label1)

    plt.legend(loc='best')
    plt.title("Predictions v.s. true values")
    plt.show()
