# Database Schema

This document provides a detailed explanation of the database schema used in the Financial Assistance Scheme Management System.

## Tables Overview

### 1. `administrators`

This table manages system administrators.

| Column Name       | Data Type | Description                              |
|-------------------|-----------|------------------------------------------|
| `id`              | `Integer` | Primary key, unique identifier           |
| `username`        | `String`  | Unique username for login                |
| `hashed_password` | `String`  | Hashed password for authentication       |
| `is_active`       | `Boolean` | Indicates if the administrator is active |

### 2. `persons`

This table stores personal information for all individuals.

| Column Name         | Data Type                | Description                                      |
|---------------------|--------------------------|--------------------------------------------------|
| `id`                | `Integer`                | Primary key, unique identifier                   |
| `name`              | `String`                 | Name of the individual                           |
| `ic_number`         | `String`                 | Unique identification number                     |
| `date_of_birth`     | `Date`                   | Date of birth                                    |
| `sex`               | `Enum(Sex)`              | Gender of the individual (Male/Female)           |
| `employment_status` | `Enum(EmploymentStatus)` | Employment status (Employed/Unemployed)          |
| `marital_status`    | `Enum(MaritalStatus)`    | Marital status (Single/Married/Divorced/Widowed) |

### 3. `households`

This table groups individuals into households.

| Column Name | Data Type | Description                         |
|-------------|-----------|-------------------------------------|
| `id`        | `Integer` | Primary key, unique identifier      |
| `address`   | `String`  | Address of the household            |

### 4. `household_members`

This table links individuals to households with their relationship to the applicant.

| Column Name             | Data Type | Description                                 |
|-------------------------|-----------|---------------------------------------------|
| `id`                    | `Integer` | Primary key, unique identifier              |
| `household_id`          | `Integer` | Foreign key to the `households` table       |
| `person_id`             | `Integer` | Foreign key to the `persons` table          |
| `relation_to_applicant` | `String`  | Relationship of the person to the applicant |

### 5. `schemes`

This table stores financial schemes and their eligibility criteria.

| Column Name                  | Data Type                | Description                                                |
|------------------------------|--------------------------|------------------------------------------------------------|
| `id`                         | `Integer`                | Primary key, unique identifier                             |
| `name`                       | `String`                 | Name of the financial scheme                               |
| `description`                | `String`                 | Description of the scheme                                  |
| `marital_status_required`    | `Enum(MaritalStatus)`    | Required marital status for eligibility                    |
| `employment_status_required` | `Enum(EmploymentStatus)` | Required employment status for eligibility                 |
| `required_relationships`     | `JSON`                   | List of required relationships (e.g., ["Spouse", "Child"]) |
| `household_size`             | `Integer`                | Required household size for eligibility                    |

### 6. `applicants`

This table links individuals who have applied for schemes to their `Person` and `Household` records.

| Column Name    | Data Type | Description                           |
|----------------|-----------|---------------------------------------|
| `id`           | `Integer` | Primary key, unique identifier        |
| `person_id`    | `Integer` | Foreign key to the `persons` table    |
| `household_id` | `Integer` | Foreign key to the `households` table |

### 7. `applications`

This table tracks specific applications with their submission dates.

| Column Name        | Data Type                 | Description                                                   |
|--------------------|---------------------------|---------------------------------------------------------------|
| `id`               | `Integer`                 | Primary key, unique identifier                                |
| `applicant_id`     | `Integer`                 | Foreign key to the `applicants` table                         |
| `scheme_id`        | `Integer`                 | Foreign key to the `schemes` table                            |
| `application_date` | `DateTime`                | The date when the application was submitted                   |
| `status`           | `Enum(ApplicationStatus)` | Current status of the application (Pending/Approved/Rejected) |

### 8. `benefits`

This table describes the benefits associated with each scheme.

| Column Name      | Data Type  | Description                                      |
|------------------|------------|--------------------------------------------------|
| `id`             | `Integer`  | Primary key, unique identifier                   |
| `scheme_id`      | `Integer`  | Foreign key to the `schemes` table               |
| `description`    | `String`   | Description of the benefit                       |
| `amount`         | `Integer`  | Monetary value of the benefit (if applicable)    |
| `condition`      | `String`   | Conditions for receiving the benefit             |

## Relationships Between Tables

- **Person to HouseholdMember**: A `Person` can be linked to a `Household` through the `household_members` table, specifying their relationship to the applicant.
- **Applicant to Person**: An `Applicant` is linked to a `Person`, and the same `Person` can be linked to multiple `Applicants`.
- **Scheme to Benefit**: A `Scheme` can have multiple `Benefits` associated with it, defined in the `benefits` table.
- **Application to Scheme and Applicant**: An `Application` links an `Applicant` to a `Scheme`, tracking the status and date of submission.

