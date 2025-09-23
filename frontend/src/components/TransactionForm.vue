<template>
  <div>
    <h2>Add Transaction</h2>
    <form @submit.prevent="submitTransaction">
      <label>Loan ID:</label>
      <input v-model.number="transaction.loan_id" type="number" required />

      <label>Date (YYYY-MM-DD):</label>
      <input v-model="transaction.date" type="date" required />

      <label>Amount:</label>
      <input v-model.number="transaction.amount" type="number" step="0.01" required />

      <label>Type (payment or repayment):</label>
      <select v-model="transaction.type" required>
        <option value="">Select type</option>
        <option value="payment">Payment</option>
        <option value="repayment">Repayment</option>
      </select>

      <button type="submit">Add Transaction</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      transaction: {
        loan_id: null,
        date: '',
        amount: null,
        type: ''
      },
      message: ''
    }
  },
  methods: {
    submitTransaction() {
      const backendUrl = 'http://localhost:5000'
      fetch(`${backendUrl}/transactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.transaction)
      })
        .then(res => {
          if (!res.ok) throw new Error('Failed to add transaction')
          return res.json()
        })
        .then(data => {
          this.message = `Transaction added with ID: ${data.id}`
          this.transaction = { loan_id: null, date: '', amount: null, type: '' }
        })
        .catch(err => {
          this.message = 'Error: ' + err.message
        })
    }
  }
}
</script>
