import { createResource, createListResource } from "frappe-ui"
import { userResource } from "./user"

export const unreadNotificationsCount = createResource({
	url: "artech_hrms.api.get_unread_notifications_count",
	cache: "artech_hrms:unread_notifications_count",
	initialData: 0,
	auto: true,
})

export const notifications = createListResource({
	doctype: "PWA Notification",
	filters: { to_user: userResource.data.name },
	fields: [
		"name",
		"from_user",
		"message",
		"read",
		"creation",
		"reference_document_type",
		"reference_document_name",
	],
	auto: false,
	cache: "artech_hrms:notifications",
	orderBy: "creation desc",
	onSuccess() {
		unreadNotificationsCount.reload()
	},
})

export const arePushNotificationsEnabled = createResource({
	url: "artech_hrms.api.are_push_notifications_enabled",
	cache: "artech_hrms:push_notifications_enabled",
	auto: true,
})
