<template>
  <div id="app">
    <BorrowerList />
    <LoanForm />
    <TransactionForm />
  </div>
</template>

<script>
import BorrowerList from './components/BorrowerList.vue'
import LoanForm from './components/LoanForm.vue'
import TransactionForm from './components/TransactionForm.vue'

export default {
  name: 'App',
  components: {
    BorrowerList,
    LoanForm,
    TransactionForm
  }
}
</script>
