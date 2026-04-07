using TMPro;
using UnityEngine;

public class ProfilePanelController : MonoBehaviour
{
    [Header("Texts")]
    [SerializeField] private TMP_Text nicknameText;
    [SerializeField] private TMP_Text emailText;
    [SerializeField] private TMP_Text levelText;
    [SerializeField] private TMP_Text xpText;
    [SerializeField] private TMP_Text softCurrencyText;
    [SerializeField] private TMP_Text statusText;

    public void SetLoading()
    {
        statusText.text = "Загрузка профиля...";
    }

    public void SetError(string message)
    {
        statusText.text = "Ошибка: " + message;
    }

    public void SetProfile(ProfileResponseData data)
    {
        nicknameText.text = $"Ник: {data.user.nickname}";
        emailText.text = $"Email: {data.user.email}";
        levelText.text = $"Уровень: {data.progress.level}";
        xpText.text = $"XP: {data.progress.xp}";
        softCurrencyText.text = $"Монеты: {data.progress.softCurrency}";
        statusText.text = "Профиль загружен";
    }
}