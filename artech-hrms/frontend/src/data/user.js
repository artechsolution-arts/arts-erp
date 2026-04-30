import router from "@/router"
import { createResource } from "frappe-ui"

export const userResource = createResource({
	url: "artech_hrms.api.get_current_user_info",
	cache: "artech_hrms:user",
	onError(error) {
		if (error && error.exc_type === "AuthenticationError") {
			router.push({ name: "Login" })
		}
	},
})
