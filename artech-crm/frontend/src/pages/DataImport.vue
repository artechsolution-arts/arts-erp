<template>
  <DataImport
    :doctype="route.params.doctype"
    :importName="route.params.importName"
    :doctypeMap="doctypeMap"
  />
</template>

<script setup>
import { usePageMeta } from 'frappe-ui'
import { DataImport } from 'frappe-ui/artech_engine'
import { useRoute } from 'vue-router'

const route = useRoute()

const doctypeMap = {
  'CRM Lead': {
    title: 'Leads',
    listRoute: '/artech_crm/leads',
    pageRoute: `/artech_crm/leads/docname`,
  },
  'CRM Deal': {
    title: 'Deals',
    listRoute: '/artech_crm/deals',
    pageRoute: `/artech_crm/deals/docname`,
  },
  Contact: {
    title: 'Contacts',
    listRoute: '/artech_crm/contacts',
    pageRoute: `/artech_crm/contacts/docname`,
  },
  'CRM Task': {
    title: 'Tasks',
    listRoute: '/artech_crm/tasks',
  },
  'CRM Organization': {
    title: 'Organizations',
    listRoute: '/artech_crm/organizations',
    pageRoute: `/artech_crm/organizations/docname`,
  },
  'CRM Call Log': {
    title: 'Call Log',
    listRoute: '/artech_crm/call-logs',
  },
}

usePageMeta(() => {
  return {
    title: __('Data Import'),
  }
})
</script>
