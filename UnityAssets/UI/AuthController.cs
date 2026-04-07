using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class AuthController : MonoBehaviour
{
    [SerializeField] private ApiClient apiClient;
    [SerializeField] private TMP_InputField emailInput;
    [SerializeField] private TMP_InputField passwordInput;
    [SerializeField] private TMP_Text statusText;

    public void Login()
    {
        string email = emailInput.text.Trim();
        string password = passwordInput.text;

        if (string.IsNullOrEmpty(email) || string.IsNullOrEmpty(password))
        {
            statusText.text = "Введите email и пароль";
            return;
        }

        statusText.text = "Выполняется вход...";

        LoginRequest request = new LoginRequest
        {
            email = email,
            password = password
        };

        StartCoroutine(apiClient.Post<LoginRequest, LoginResponseData>(
            "/api/v1/auth/login",
            request,
            onSuccess: data =>
            {
                apiClient.SetToken(data.accessToken);
                statusText.text = "Вход выполнен";
                SceneManager.LoadScene("MainMenu");
            },
            onError: error =>
            {
                statusText.text = $"{error.code}: {error.message}";
            }
        ));
    }
}