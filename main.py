from altman import Altman
from merton import Merton
from financial_statements import Companies
from visualization import print_ratios, print_z_scores, z_score_plot



def main():

    print("Starting data processing...\n")

    companies = Companies(
        ["VZ", "MA", "BA", "F"],
        interval="1y"
    )

    # ---------- ALTAMN MODEL ----------
    
    altman = Altman(companies)

    # ---------- PRINTS ----------
    print_ratios(altman)
    print_z_scores(altman)

    # ---------- PLOT ----------
    z_df = altman.z_scores_df()
    #z_score_plot(z_df, title="Altman Z-Scores Visualization")
    
    # ---------- Merton Model ----------
    merton = Merton(companies)
    
    ## ---------- PRINTS ----------
    merton_df = merton.merton_df()
    print("\n=== Merton Model Results ===")
    print(merton_df)

if __name__ == "__main__":
    main()