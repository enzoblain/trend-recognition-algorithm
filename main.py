from algorithm.algo import trend_recognition

from pandas import read_csv

def main():
    print(trend_recognition(read_csv('data/data_test.csv')))
    return 

if __name__ == "__main__":    
    main()