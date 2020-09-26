# HouseholdApplience

 扎尼克

## Case study 2.1

As a user, I want to be able to manage my household appliances so that I could properly document and
maintain them.

### Acceptance Criteria:

- Searchable list of all recorded appliances
  - Can be filtered using the provided search filters
    - Serial Number
    - Brand
    - Model
    - Status
    - Date Bought
- Create a new record of my appliance not found in the list
   - System will show an error message if the same appliance is already found by identifying:
    - Serial Number
    - Brand
    - Model
- Update the details of an appliance
  - Serial Number
  - Brand
  - Model
  - Date Bought
  - Status
- Remove old/unused/sold appliance from the list
- UI should be properly viewable in any devices (mobile, desktop, tablet, etc.)


### Definition of Done:

- Code Reviewed
- Passed Unit Tests
- Provided demo user for live testing
- User Frontend deployed in a cloud provider and able to communicate to the Backend service
- Backend service deployed in another cloud provider
- Source codes available for review in a source code repository

### Technical Requirements:

- Frontend:
  - Any web technology/framework/library your most comfortable to use
  - Should be able to communicate to the backend using secured HTTP protocol
- Backend
  - Use Go programming language
  - Any frameworks to use for the backend