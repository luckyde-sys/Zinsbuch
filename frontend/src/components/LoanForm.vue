<template>
  <div>
    <h2>Add Loan</h2>
    <form @submit.prevent="submitLoan">
      <label>Borrower ID:</label>
      <input v-model.number="loan.borrower_id" type="number" required />

      <label>Principal:</label>
      <input v-model.number="loan.principal" type="number" step="0.01" required />

      <label>Rate (%):</label>
      <input v-model.number="loan.rate" type="number" step="0.01" required />

      <label>Date (YYYY-MM-DD):</label>
      <input v-model="loan.date" type="date" required />

      <label>Description:</label>
      <input v-model="loan.description" type="text" />

      <button type="submit">Add Loan</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loan: {
        borrower_id: null,
        principal: null,
        rate: null,
        date: '',
        description: ''
      },
      message: ''
    }
  },
  methods: {
    submitLoan() {
      const backendUrl = 'http://localhost:5000'
      fetch(`${backendUrl}/loans`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.loan)
      })
        .then(res => {
          if (!res.ok) throw new Error('Failed to add loan')
          return res.json()
        })
        .then(data => {
          this.message = `Loan added with ID: ${data.id}`
          this.loan = { borrower_id: null, principal: null, rate: null, date: '', description: '' }
        })
        .catch(err => {
          this.message = 'Error: ' + err.message
        })
    }
  }
}
</script>
