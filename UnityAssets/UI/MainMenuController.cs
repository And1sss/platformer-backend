using UnityEngine;

public class MainMenuController : MonoBehaviour
{
    [SerializeField] private ApiClient apiClient;
    [SerializeField] private ProfilePanelController profilePanel;
    [SerializeField] private LeaderboardPanelController leaderboardPanel;

    private void Start()
    {
        apiClient.LoadSavedToken();
        Debug.Log("MainMenu token: " + apiClient.AccessToken);

        if (string.IsNullOrEmpty(apiClient.AccessToken))
        {
            profilePanel.SetError("Нет токена. Сначала войди.");
            LoadLeaderboard();
            return;
        }

        LoadProfile();
        LoadLeaderboard();
    }

    public void LoadProfile()
    {
        profilePanel.SetLoading();

        StartCoroutine(apiClient.Get<ProfileResponseData>(
            "/api/v1/profile",
            onSuccess: data =>
            {
                profilePanel.SetProfile(data);
            },
            onError: error =>
            {
                if (error.code == "UNAUTHORIZED" || error.code == "HTTP_ERROR")
                {
                    apiClient.ClearToken();
                }

                profilePanel.SetError($"{error.code}: {error.message}");
            }
        ));
    }

    public void LoadLeaderboard()
    {
        if (leaderboardPanel == null)
        {
            Debug.LogError("LeaderboardPanel is not assigned");
            return;
        }

        leaderboardPanel.SetLoading();

        StartCoroutine(apiClient.Get<LeaderboardResponseData>(
            "/api/v1/leaderboard?boardCode=platformer_score&season=1&limit=10",
            onSuccess: data =>
            {
                leaderboardPanel.SetLeaderboard(data);
            },
            onError: error =>
            {
                leaderboardPanel.SetError($"{error.code}: {error.message}");
            }
        ));
    }

    public void RefreshAll()
    {
        LoadProfile();
        LoadLeaderboard();
    }
}