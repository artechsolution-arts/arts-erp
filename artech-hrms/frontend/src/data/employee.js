import router from "@/router"
import { createResource } from "frappe-ui"

export const employeeResource = createResource({
	url: "artech_hrms.api.get_current_employee_info",
	cache: "artech_hrms:employee",
	onError(error) {
		if (error && error.exc_type === "AuthenticationError") {
			router.push("/login")
		}
	},
})
