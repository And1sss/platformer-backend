using System.Text;
using TMPro;
using UnityEngine;

public class LeaderboardPanelController : MonoBehaviour
{
    [SerializeField] private TMP_Text leaderboardContentText;
    [SerializeField] private TMP_Text statusText;

    public void SetLoading()
    {
        if (statusText != null)
            statusText.text = "Загрузка лидерборда...";

        if (leaderboardContentText != null)
            leaderboardContentText.text = "";
    }

    public void SetError(string message)
    {
        if (statusText != null)
            statusText.text = "Ошибка лидерборда: " + message;
    }

    public void SetLeaderboard(LeaderboardResponseData data)
    {
        if (statusText != null)
            statusText.text = "Лидерборд загружен";

        if (leaderboardContentText == null) return;

        if (data.items == null || data.items.Count == 0)
        {
            leaderboardContentText.text = "Пока нет результатов";
            return;
        }

        StringBuilder sb = new StringBuilder();

        foreach (var item in data.items)
        {
            sb.AppendLine($"{item.rank}. {item.nickname} - {item.score}");
        }

        leaderboardContentText.text = sb.ToString();
    }
}