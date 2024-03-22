/* 
Use the http package to make HTTP requests to the backend server to retrieve transaction data. 
For example, you might use the fetch() function to retrieve a list of transactions for a user or a specific account.
*/

import java.net.HttpURLConnection
import java.net.URL
import org.json.JSONArray
import org.json.JSONObject
import com.Split.TransactionDatabase
import java.time.LocalDate
import java.time.format.DateTimeFormatter

data class Transaction(
    val id: Int,
    val date: LocalDate,
    val amount: Double,
    val description: String
)

fun fetchTransactions(userId: Int): List<Transaction> {
    val url = URL("https://example.com/api/transactions?userId=$userId")
    val connection = url.openConnection() as HttpURLConnection
    connection.requestMethod = "GET"

    val transactions = mutableListOf<Transaction>()

    if (connection.responseCode == HttpURLConnection.HTTP_OK) {
        val inputStream = connection.inputStream
        val jsonData = inputStream.bufferedReader().use { it.readText() }
        val jsonArray = JSONArray(jsonData)

        for (i in 0 until jsonArray.length()) {
            val jsonObject = jsonArray.getJSONObject(i)
            val id = jsonObject.getInt("id")
            val dateString = jsonObject.getString("date")
            val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
            val date = LocalDate.parse(dateString, dateFormat)
            val amount = jsonObject.getDouble("amount")
            val description = jsonObject.getString("description")

            transactions.add(Transaction(id, date, amount, description))
        }
    } else {
        println("Error: ${connection.responseCode} ${connection.responseMessage}")
    }

    connection.disconnect()
    return transactions
}

