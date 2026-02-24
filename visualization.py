
from libraries import px , plt , st



def plot_altman(z_df):

    fig, ax = plt.subplots(figsize=(8,5))

    ax.bar(z_df.index, z_df["Z-Score"])

    ax.axhline(1.81, linestyle="--")
    ax.axhline(2.99, linestyle="--")

    ax.set_title("Altman Z-Score")
    ax.set_ylabel("Z Score")
    ax.set_xlabel("Ticker")

    ax.grid(alpha=0.3)

    st.pyplot(fig)


def plot_merton_dd(merton_df):

    fig, ax = plt.subplots(figsize=(8,5))

    ax.bar(
        merton_df.index,
        merton_df["Distance to Default"]
    )

    ax.set_title("Distance to Default")
    ax.set_ylabel("DD")
    ax.grid(alpha=0.3)

    st.pyplot(fig)


def plot_pd(merton_df):

    fig, ax = plt.subplots(figsize=(8,5))

    ax.bar(
        merton_df.index,
        merton_df["Probability of Default"]
    )

    ax.set_title("Probability of Default (%)")
    ax.set_ylabel("PD %")
    ax.grid(alpha=0.3)

    st.pyplot(fig)


# ==========================================
    
'''
def z_score_plot(z_df, title="Altman Z-Scores"):

    z_df = z_df.reset_index()
    z_df = z_df.sort_values("Z-Score")

    colors = []

    for z in z_df["Z-Score"]:
        if z < 1.81:
            colors.append("#ba1e1e")
        elif z < 2.99:
            colors.append("#b4c2c3")
        else:
            colors.append("#6fee8b")

    plt.figure(figsize=(10,6))

    plt.bar(
        z_df["Ticker"],
        z_df["Z-Score"],
        color=colors
    )

    plt.axhline(1.8, linestyle="--", color = "#ba1e1e")
    plt.axhline(3, linestyle="--", color = "#1c682c")

    plt.title(title)
    plt.ylabel("Z-Score")
    plt.xlabel("Ticker")
    plt.legend(["Unsafe", "Safe"])
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

'''