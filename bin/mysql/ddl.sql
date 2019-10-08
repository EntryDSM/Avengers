DROP SCHEMA IF EXISTS entrydsm ;

CREATE SCHEMA IF NOT EXISTS entrydsm DEFAULT CHARACTER SET utf8mb4 ;
USE entrydsm ;

create table if not exists school
(
    code             varchar(10)  not null
        primary key,
    school_name      varchar(50)  not null,
    school_full_name varchar(100) null,
    education_office varchar(50)  null
)
    collate = utf8mb4_unicode_ci;


create table if not exists user
(
    email    varchar(100) not null
        primary key,
    password varchar(100) not null,
    receipt_code                   int not null,
    is_paid                        tinyint(1) default 0 null,
    is_printed_application_arrived tinyint(1) default 0 null,
    is_passed_first_apply          tinyint(1) default 0 null,
    is_passed_interview            tinyint(1) default 0 null,
    is_final_submit                tinyint(1) default 0 null,
    exam_code                      varchar(6)        null,
    volunteer_score  decimal(10, 5) null,
    attendance_score int            null,
    conversion_score decimal(10, 5) null,
    final_score      decimal(10, 5) null
)
    collate = utf8mb4_unicode_ci;


create table if not exists ged_application
(
    user_email        varchar(100)                                                                                                                                                           not null
        primary key,
    apply_type        varchar(45) null,
    additional_type   varchar(45) null,
    is_daejeon        tinyint(1)                                                                                                                                                                null,
    name              varchar(15)                                                                                                                                                            null,
    sex               varchar(45) null,
    birth_date        date                                                                                                                                                                   null,
    parent_name       varchar(15)                                                                                                                                                            null,
    parent_tel        varchar(9)                                                                                                                                                             null,
    applicant_tel     varchar(9)                                                                                                                                                             null,
    address           varchar(500)                                                                                                                                                           null,
    post_code         varchar(5)                                                                                                                                                             null,
    ged_average_score decimal(10, 5)                                                                                                                                                         null,
    self_introduction varchar(1600)                                                                                                                                                          null,
    study_plan        varchar(1600)                                                                                                                                                          null
)
    collate = utf8mb4_unicode_ci;

create table if not exists graduated_application
(
    user_email        varchar(100)                                                                                                                                                           not null
        primary key,
    apply_type        varchar(45) null,
    additional_type    varchar(45) null,
    is_daejeon        tinyint(1)                                                                                                                                                                null,
    name              varchar(15)                                                                                                                                                            null,
    sex               varchar(45) null,
    birth_date        date                                                                                                                                                                   null,
    parent_name       varchar(15)                                                                                                                                                            null,
    parent_tel        varchar(9)                                                                                                                                                             null,
    applicant_tel     varchar(9)                                                                                                                                                             null,
    address           varchar(500)                                                                                                                                                           null,
    post_code         varchar(5)                                                                                                                                                             null,
    student_number    varchar(5)                                                                                                                                                             null,
    graduated_year    varchar(4)                                                                                                                                                             null,
    school_code       varchar(10)                                                                                                                                                            null,
    school_tel        varchar(9)                                                                                                                                                             null,
    volunteer_time    int                                                                                                                                                                    null,
    full_cut_count    int                                                                                                                                                                    null,
    period_cut_count  int                                                                                                                                                                    null,
    late_count        int                                                                                                                                                                    null,
    early_leave_count int                                                                                                                                                                    null,
    korean            varchar(6)                                                                                                                                                             null,
    social            varchar(6)                                                                                                                                                             null,
    history           varchar(6)                                                                                                                                                             null,
    math              varchar(6)                                                                                                                                                             null,
    science           varchar(6)                                                                                                                                                             null,
    tech_and_home     varchar(6)                                                                                                                                                             null,
    english           varchar(6)                                                                                                                                                             null,
    self_introduction   varchar(1600)                                                                                                                                                         null,
    study_plan          varchar(1600)                                                                                                                                                          null,
    first_grade_score  decimal(10, 5) null,
    second_grade_score  decimal(10, 5) null,
    third_grade_score  decimal(10, 5) null,
)
    collate = utf8mb4_unicode_ci;


create table if not exists ungraduated_application
(
    user_email        varchar(100)                                                                                                                                                           not null
        primary key,
    apply_type        varchar(45) null,
    additional_type   varchar(45) null,
    is_daejeon        tinyint(1)                                                                                                                                                                null,
    name              varchar(15)                                                                                                                                                            null,
    sex               varchar(45) null,
    birth_date        date                                                                                                                                                                   null,
    parent_name       varchar(15)                                                                                                                                                            null,
    parent_tel        varchar(9)                                                                                                                                                             null,
    applicant_tel     varchar(9)                                                                                                                                                             null,
    address           varchar(500)                                                                                                                                                           null,
    post_code         varchar(5)                                                                                                                                                             null,
    student_number    varchar(5)                                                                                                                                                             null,
    school_code       varchar(10)                                                                                                                                                            null,
    school_tel        varchar(9)                                                                                                                                                             null,
    volunteer_time    int                                                                                                                                                                    null,
    full_cut_count    int                                                                                                                                                                    null,
    period_cut_count  int                                                                                                                                                                    null,
    late_count        int                                                                                                                                                                    null,
    early_leave_count int                                                                                                                                                                    null,
    korean            varchar(5)                                                                                                                                                             null,
    social            varchar(5)                                                                                                                                                             null,
    history           varchar(5)                                                                                                                                                             null,
    math              varchar(5)                                                                                                                                                             null,
    science           varchar(5)                                                                                                                                                             null,
    tech_and_home     varchar(5)                                                                                                                                                             null,
    english           varchar(5)                                                                                                                                                             null,
    self_introduction  varchar(1600)                                                                                                                                                          null,
    study_plan        varchar(1600)                                                                                                                                                          null
)
    collate = utf8mb4_unicode_ci;

