PGDMP         1                {            fastapi    15.1    15.1 S    ~           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    fastapi    DATABASE     �   CREATE DATABASE fastapi WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE fastapi;
                postgres    false            �            1259    32826    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    139938    companys    TABLE     �  CREATE TABLE public.companys (
    id integer NOT NULL,
    company_name character varying NOT NULL,
    company_code character varying NOT NULL,
    created_date timestamp with time zone DEFAULT now() NOT NULL,
    created_by character varying NOT NULL,
    modified_date timestamp with time zone,
    modified_by character varying,
    opening_date timestamp with time zone DEFAULT now()
);
    DROP TABLE public.companys;
       public         heap    postgres    false            �            1259    139937    companys_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.companys_id_seq;
       public          postgres    false    218            �           0    0    companys_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.companys_id_seq OWNED BY public.companys.id;
          public          postgres    false    217            �            1259    139965    menu_permission    TABLE     �  CREATE TABLE public.menu_permission (
    id integer NOT NULL,
    pms_menu_name character varying NOT NULL,
    pms_menu_level integer,
    pms_parent_id integer,
    to_name character varying NOT NULL,
    pms_menu_type integer,
    pms_menu_index integer,
    pms_menu_image character varying,
    created_date timestamp with time zone DEFAULT now(),
    created_by character varying,
    modified_date timestamp with time zone,
    modified_by character varying,
    db_id integer
);
 #   DROP TABLE public.menu_permission;
       public         heap    postgres    false            �            1259    139964    menu_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.menu_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.menu_permission_id_seq;
       public          postgres    false    222            �           0    0    menu_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.menu_permission_id_seq OWNED BY public.menu_permission.id;
          public          postgres    false    221            �            1259    147999    posts    TABLE       CREATE TABLE public.posts (
    id integer NOT NULL,
    title character varying NOT NULL,
    content character varying NOT NULL,
    published boolean DEFAULT true NOT NULL,
    create_date timestamp with time zone DEFAULT now() NOT NULL,
    owner_id integer NOT NULL
);
    DROP TABLE public.posts;
       public         heap    postgres    false            �            1259    147998    posts_id_seq    SEQUENCE     �   CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.posts_id_seq;
       public          postgres    false    230            �           0    0    posts_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;
          public          postgres    false    229            �            1259    140027    users    TABLE     �  CREATE TABLE public.users (
    id integer NOT NULL,
    fullname character varying NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    last_pwd_modified_date timestamp with time zone,
    phone_number character varying,
    branch_id integer NOT NULL,
    status boolean DEFAULT true NOT NULL,
    roleid integer NOT NULL,
    counterno character varying,
    created_date timestamp with time zone DEFAULT now() NOT NULL,
    created_by character varying NOT NULL,
    modified_date timestamp with time zone,
    modified_by character varying,
    description character varying,
    deviceid text,
    reset_token text,
    reset_token_expiration timestamp with time zone
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    140026    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    228            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    227            �            1259    139979    usp_branchs    TABLE     �  CREATE TABLE public.usp_branchs (
    id integer NOT NULL,
    branch_code character varying NOT NULL,
    branch_name character varying NOT NULL,
    opening_date date,
    range_ip integer NOT NULL,
    created_date timestamp with time zone DEFAULT now() NOT NULL,
    created_by character varying NOT NULL,
    modified_date timestamp with time zone,
    modified_by character varying,
    tvticketip jsonb,
    company_id integer NOT NULL
);
    DROP TABLE public.usp_branchs;
       public         heap    postgres    false            �            1259    139978    usp_branchs_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usp_branchs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.usp_branchs_id_seq;
       public          postgres    false    224            �           0    0    usp_branchs_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.usp_branchs_id_seq OWNED BY public.usp_branchs.id;
          public          postgres    false    223            �            1259    139824    usp_configuration    TABLE     C  CREATE TABLE public.usp_configuration (
    id integer NOT NULL,
    paramname character varying NOT NULL,
    value character varying,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying,
    modified_date timestamp without time zone,
    modified_by character varying
);
 %   DROP TABLE public.usp_configuration;
       public         heap    postgres    false            �            1259    139823    usp_configuration_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usp_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.usp_configuration_id_seq;
       public          postgres    false    216            �           0    0    usp_configuration_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.usp_configuration_id_seq OWNED BY public.usp_configuration.id;
          public          postgres    false    215            �            1259    139951    usp_role    TABLE     ?  CREATE TABLE public.usp_role (
    id integer NOT NULL,
    rolecode character varying NOT NULL,
    rolename character varying NOT NULL,
    created_date timestamp with time zone DEFAULT now() NOT NULL,
    created_by character varying,
    modified_date timestamp with time zone,
    modified_by character varying
);
    DROP TABLE public.usp_role;
       public         heap    postgres    false            �            1259    139950    usp_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usp_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.usp_role_id_seq;
       public          postgres    false    220            �           0    0    usp_role_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.usp_role_id_seq OWNED BY public.usp_role.id;
          public          postgres    false    219            �            1259    139996    usp_rule_npms_assign    TABLE     �  CREATE TABLE public.usp_rule_npms_assign (
    id integer NOT NULL,
    roleid integer NOT NULL,
    pmsid integer,
    p_view boolean DEFAULT false,
    p_view_data boolean DEFAULT false NOT NULL,
    p_refresh boolean DEFAULT false NOT NULL,
    p_search boolean DEFAULT false NOT NULL,
    p_add boolean DEFAULT false NOT NULL,
    p_edit boolean DEFAULT false NOT NULL,
    p_delete boolean DEFAULT false NOT NULL,
    p_save boolean DEFAULT false NOT NULL,
    p_print boolean DEFAULT false NOT NULL,
    p_import boolean DEFAULT false NOT NULL,
    p_export boolean DEFAULT false NOT NULL,
    created_date timestamp with time zone DEFAULT now(),
    created_by character varying,
    modified_date date,
    modified_by character varying
);
 (   DROP TABLE public.usp_rule_npms_assign;
       public         heap    postgres    false            �            1259    139995    usp_rule_npms_assign_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usp_rule_npms_assign_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.usp_rule_npms_assign_id_seq;
       public          postgres    false    226            �           0    0    usp_rule_npms_assign_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.usp_rule_npms_assign_id_seq OWNED BY public.usp_rule_npms_assign.id;
          public          postgres    false    225            �            1259    148014    votes    TABLE     Z   CREATE TABLE public.votes (
    post_id integer NOT NULL,
    user_id integer NOT NULL
);
    DROP TABLE public.votes;
       public         heap    postgres    false            �           2604    139941    companys id    DEFAULT     j   ALTER TABLE ONLY public.companys ALTER COLUMN id SET DEFAULT nextval('public.companys_id_seq'::regclass);
 :   ALTER TABLE public.companys ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            �           2604    139968    menu_permission id    DEFAULT     x   ALTER TABLE ONLY public.menu_permission ALTER COLUMN id SET DEFAULT nextval('public.menu_permission_id_seq'::regclass);
 A   ALTER TABLE public.menu_permission ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    222    222            �           2604    148002    posts id    DEFAULT     d   ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);
 7   ALTER TABLE public.posts ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    229    230    230            �           2604    140030    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    227    228    228            �           2604    139982    usp_branchs id    DEFAULT     p   ALTER TABLE ONLY public.usp_branchs ALTER COLUMN id SET DEFAULT nextval('public.usp_branchs_id_seq'::regclass);
 =   ALTER TABLE public.usp_branchs ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223    224            �           2604    139827    usp_configuration id    DEFAULT     |   ALTER TABLE ONLY public.usp_configuration ALTER COLUMN id SET DEFAULT nextval('public.usp_configuration_id_seq'::regclass);
 C   ALTER TABLE public.usp_configuration ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216            �           2604    139954    usp_role id    DEFAULT     j   ALTER TABLE ONLY public.usp_role ALTER COLUMN id SET DEFAULT nextval('public.usp_role_id_seq'::regclass);
 :   ALTER TABLE public.usp_role ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219    220            �           2604    139999    usp_rule_npms_assign id    DEFAULT     �   ALTER TABLE ONLY public.usp_rule_npms_assign ALTER COLUMN id SET DEFAULT nextval('public.usp_rule_npms_assign_id_seq'::regclass);
 F   ALTER TABLE public.usp_rule_npms_assign ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225    226            j          0    32826    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    214   �l       n          0    139938    companys 
   TABLE DATA           �   COPY public.companys (id, company_name, company_code, created_date, created_by, modified_date, modified_by, opening_date) FROM stdin;
    public          postgres    false    218   �l       r          0    139965    menu_permission 
   TABLE DATA           �   COPY public.menu_permission (id, pms_menu_name, pms_menu_level, pms_parent_id, to_name, pms_menu_type, pms_menu_index, pms_menu_image, created_date, created_by, modified_date, modified_by, db_id) FROM stdin;
    public          postgres    false    222   �n       z          0    147999    posts 
   TABLE DATA           U   COPY public.posts (id, title, content, published, create_date, owner_id) FROM stdin;
    public          postgres    false    230   kr       x          0    140027    users 
   TABLE DATA             COPY public.users (id, fullname, username, email, password, last_pwd_modified_date, phone_number, branch_id, status, roleid, counterno, created_date, created_by, modified_date, modified_by, description, deviceid, reset_token, reset_token_expiration) FROM stdin;
    public          postgres    false    228   �r       t          0    139979    usp_branchs 
   TABLE DATA           �   COPY public.usp_branchs (id, branch_code, branch_name, opening_date, range_ip, created_date, created_by, modified_date, modified_by, tvticketip, company_id) FROM stdin;
    public          postgres    false    224   ut       l          0    139824    usp_configuration 
   TABLE DATA           w   COPY public.usp_configuration (id, paramname, value, created_date, created_by, modified_date, modified_by) FROM stdin;
    public          postgres    false    216   �u       p          0    139951    usp_role 
   TABLE DATA           p   COPY public.usp_role (id, rolecode, rolename, created_date, created_by, modified_date, modified_by) FROM stdin;
    public          postgres    false    220   �v       v          0    139996    usp_rule_npms_assign 
   TABLE DATA           �   COPY public.usp_rule_npms_assign (id, roleid, pmsid, p_view, p_view_data, p_refresh, p_search, p_add, p_edit, p_delete, p_save, p_print, p_import, p_export, created_date, created_by, modified_date, modified_by) FROM stdin;
    public          postgres    false    226   �w       {          0    148014    votes 
   TABLE DATA           1   COPY public.votes (post_id, user_id) FROM stdin;
    public          postgres    false    231   �{       �           0    0    companys_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.companys_id_seq', 35, true);
          public          postgres    false    217            �           0    0    menu_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.menu_permission_id_seq', 37, true);
          public          postgres    false    221            �           0    0    posts_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.posts_id_seq', 1, false);
          public          postgres    false    229            �           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 67, true);
          public          postgres    false    227            �           0    0    usp_branchs_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.usp_branchs_id_seq', 33, true);
          public          postgres    false    223            �           0    0    usp_configuration_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.usp_configuration_id_seq', 8, true);
          public          postgres    false    215            �           0    0    usp_role_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.usp_role_id_seq', 32, true);
          public          postgres    false    219            �           0    0    usp_rule_npms_assign_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.usp_rule_npms_assign_id_seq', 327, true);
          public          postgres    false    225            �           2606    32830 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    214            �           2606    139949 "   companys companys_company_name_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.companys
    ADD CONSTRAINT companys_company_name_key UNIQUE (company_name);
 L   ALTER TABLE ONLY public.companys DROP CONSTRAINT companys_company_name_key;
       public            postgres    false    218            �           2606    139947    companys companys_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.companys
    ADD CONSTRAINT companys_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.companys DROP CONSTRAINT companys_pkey;
       public            postgres    false    218            �           2606    139973 $   menu_permission menu_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.menu_permission
    ADD CONSTRAINT menu_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.menu_permission DROP CONSTRAINT menu_permission_pkey;
       public            postgres    false    222            �           2606    139975 1   menu_permission menu_permission_pms_menu_name_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.menu_permission
    ADD CONSTRAINT menu_permission_pms_menu_name_key UNIQUE (pms_menu_name);
 [   ALTER TABLE ONLY public.menu_permission DROP CONSTRAINT menu_permission_pms_menu_name_key;
       public            postgres    false    222            �           2606    139977 +   menu_permission menu_permission_to_name_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.menu_permission
    ADD CONSTRAINT menu_permission_to_name_key UNIQUE (to_name);
 U   ALTER TABLE ONLY public.menu_permission DROP CONSTRAINT menu_permission_to_name_key;
       public            postgres    false    222            �           2606    148008    posts posts_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_pkey;
       public            postgres    false    230            �           2606    140040    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            postgres    false    228            �           2606    140036    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    228            �           2606    140038    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    228            �           2606    139989 '   usp_branchs usp_branchs_branch_name_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.usp_branchs
    ADD CONSTRAINT usp_branchs_branch_name_key UNIQUE (branch_name);
 Q   ALTER TABLE ONLY public.usp_branchs DROP CONSTRAINT usp_branchs_branch_name_key;
       public            postgres    false    224            �           2606    139987    usp_branchs usp_branchs_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.usp_branchs
    ADD CONSTRAINT usp_branchs_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.usp_branchs DROP CONSTRAINT usp_branchs_pkey;
       public            postgres    false    224            �           2606    139834 1   usp_configuration usp_configuration_paramname_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.usp_configuration
    ADD CONSTRAINT usp_configuration_paramname_key UNIQUE (paramname);
 [   ALTER TABLE ONLY public.usp_configuration DROP CONSTRAINT usp_configuration_paramname_key;
       public            postgres    false    216            �           2606    139832 (   usp_configuration usp_configuration_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.usp_configuration
    ADD CONSTRAINT usp_configuration_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.usp_configuration DROP CONSTRAINT usp_configuration_pkey;
       public            postgres    false    216            �           2606    139959    usp_role usp_role_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usp_role
    ADD CONSTRAINT usp_role_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.usp_role DROP CONSTRAINT usp_role_pkey;
       public            postgres    false    220            �           2606    139961    usp_role usp_role_rolecode_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.usp_role
    ADD CONSTRAINT usp_role_rolecode_key UNIQUE (rolecode);
 H   ALTER TABLE ONLY public.usp_role DROP CONSTRAINT usp_role_rolecode_key;
       public            postgres    false    220            �           2606    139963    usp_role usp_role_rolename_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.usp_role
    ADD CONSTRAINT usp_role_rolename_key UNIQUE (rolename);
 H   ALTER TABLE ONLY public.usp_role DROP CONSTRAINT usp_role_rolename_key;
       public            postgres    false    220            �           2606    140015 .   usp_rule_npms_assign usp_rule_npms_assign_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.usp_rule_npms_assign
    ADD CONSTRAINT usp_rule_npms_assign_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.usp_rule_npms_assign DROP CONSTRAINT usp_rule_npms_assign_pkey;
       public            postgres    false    226            �           2606    148018    votes votes_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_pkey PRIMARY KEY (post_id, user_id);
 :   ALTER TABLE ONLY public.votes DROP CONSTRAINT votes_pkey;
       public            postgres    false    231    231            �           2606    148009    posts posts_owner_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_owner_id_fkey;
       public          postgres    false    3277    230    228            �           2606    140041    users users_branch_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.usp_branchs(id) ON UPDATE CASCADE ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.users DROP CONSTRAINT users_branch_id_fkey;
       public          postgres    false    224    228    3271            �           2606    140046    users users_roleid_fkey    FK CONSTRAINT     x   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_roleid_fkey FOREIGN KEY (roleid) REFERENCES public.usp_role(id);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_roleid_fkey;
       public          postgres    false    220    228    3257            �           2606    139990 '   usp_branchs usp_branchs_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.usp_branchs
    ADD CONSTRAINT usp_branchs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companys(id) ON UPDATE CASCADE ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.usp_branchs DROP CONSTRAINT usp_branchs_company_id_fkey;
       public          postgres    false    3255    218    224            �           2606    140021 4   usp_rule_npms_assign usp_rule_npms_assign_pmsid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.usp_rule_npms_assign
    ADD CONSTRAINT usp_rule_npms_assign_pmsid_fkey FOREIGN KEY (pmsid) REFERENCES public.menu_permission(id);
 ^   ALTER TABLE ONLY public.usp_rule_npms_assign DROP CONSTRAINT usp_rule_npms_assign_pmsid_fkey;
       public          postgres    false    3263    226    222            �           2606    140016 5   usp_rule_npms_assign usp_rule_npms_assign_roleid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.usp_rule_npms_assign
    ADD CONSTRAINT usp_rule_npms_assign_roleid_fkey FOREIGN KEY (roleid) REFERENCES public.usp_role(id);
 _   ALTER TABLE ONLY public.usp_rule_npms_assign DROP CONSTRAINT usp_rule_npms_assign_roleid_fkey;
       public          postgres    false    220    226    3257            �           2606    148019    votes votes_post_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id) ON DELETE CASCADE;
 B   ALTER TABLE ONLY public.votes DROP CONSTRAINT votes_post_id_fkey;
       public          postgres    false    3281    231    230            �           2606    148024    votes votes_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
 B   ALTER TABLE ONLY public.votes DROP CONSTRAINT votes_user_id_fkey;
       public          postgres    false    228    231    3277            j      x�37J3042O13O3����� (�      n   �  x���=O�0�9��Q+�9��l&$>�.HT*I�"!�=�]lz�Tǀ�!����=Cя���᫂�����@��lg`�@���R�x>l'(6������^F��"YGY{Yd-��(�^�r-�M����@6"��r��F 7"�F�z�
d+�]����@v"��r��V �"T�ʩ+�,Xw�k��h�·�-g�G}ZV��驌:�4�η&�S�!dhY�Oa���C�!� �:��LO!��E�adu>����!�@��|"3=�C"1K���4���:.$��h�)�x��Y"9}!�TOyǐH��������'lr�����]���°͑�sV��y��GC�0k�/��ꮸ��~����4������֯Ȼq7T��v����+�V�S���� ���O��l�d��v���v�èͺ,�o |�      r   �  x��WMo�8=ӿB�^2DR����thѴ�&�S C�h�[I��������>���>���{�������:lE&���WT�UO���&�!�B��h}K�m/�`J��V(+*^�� ��d�.x`��JqQ;��.�C�X�,�ES�0�P4��5�T�~�7 WZfZ��I�R9�l��`jUAMM��ѝ�w|� YV��=y���19M$A����إN�!�:�$��qz�n�Z1<dJ���-|������yɮ+����4���Y�ܮ�Yv��!�#d���A 6�[�vY+4Q �?��4�{v���H����m[5��ǫ#"�*��؊�װ����@�љ�UL})>����散Zj�"�V+�Z�L�x�b�<_-A.����B�Z�Vj�/�88�mT'�����T>hO?�|Y+t� _m�u�G�ur-?�Чʐ?x�����ɮ1Z����[m
��b$��6�Q�<��X����`��/�r ����R�M��
ԇ���Ћ�O?��ho��~��n��LS�O�
�5@�z�^��Y^�mHֿ��1�y�cIR�~'d�~th\#��_m��g��K���v ̇�ժM��g:�fʴR�]�̔�U풸J)Q�"������a�嶩���
��S:���8�!ܣ���qi�F��U��z�,�&��	��m�{�t�^���*�=�\�*�K��N���V����s�A7E�1Ђf�"�P)򟡝�&���gu36�Az��y��j0hN��	*ى��w�n����59+4�,��&�7#@b��gF^�8��[�o�$Q���K����ۦn�&x�� 挔4vlN�W�oÜ8���W�߄9��i����C����b���!���
��J8���)a�A-�
��b7Lg��g���*��P�t�DQ�V���b��_�
�      z      x������ � �      x   �  x���Ko�0���Wd�n��u�WV��%T�L )�T݄�H&BZ��OxLi�r,[>����m���񼀓��訿�EE4K�iT��M�(��&�6�4������<[�{o�>��T�#dڎ� ��mG,̢Q�����9�&F�E�`��21�@$�0�  !DmS��_g?���XZ[f8;��Y����t0-RoYgJz��;���ƴ@�z���Li��B�ʯ������I���?+c��e�a�[��M0xY�q��(Y9A�ڃ��<'iar`nQD���ud'��_�V�o�~A��\�>����$�s�5?\�e�T�>��dc�����Y��,{J&�U{LҾj�ɗC��e'类f��^��̢a
����<�J�V�����Ѝ���������rl�;�h�V*�l�|��C�Ym='{z.���<����C
bHy���g���`���@��8g�W�h4� 	��      t   I  x����j�0E��Wd_l桧����.ōbH�b5��+�)��j<F3:�j$TS?����C��_2��9! �jD� ��}�1@���:�̈́j��V$�$�$��0]�T���l�,k	��g;�ұ�`#�f�c#[	�lg;�ұ�`'�n6�I��`�D�t�8��k4t�m� p�v��0n7���}y�^�-_  �xRz�Ŕ�!F*�Eץq����\�K5^�.�աP7�A6�o�����lx�A|�#l�6V3�y£�R*AP�RM��Zh�g8w˺��E��Ȥ�ο�,��P������@�VMUU?
$�      l   �   x��ѱn�0���T�D>�	I�J��,>Z��F�Q��	Q�.a�������<�K����#��/�Xci���f���MO���#��������5�y�&e�F���|��_;(�O�MS����O���GUp��k6�"�7įW��'˃dݹQ������j��(�SȬ!E�)Ffa��P��u׶Y�a�A��8c[WUu�)�
      p   �   x��ѱj�0���ރ��N�m!��5v�)�!*1%v��B߾��B;
����	��=<Aw���;]�HJ]Jm
���iR�6��6��~����DW5�K�)dhN�3���y��欕����m\|�+�m����`�k���mo�G����8�2�rI������7F�O�Ч#:��%��i�,)�[�mr!��4�����+��o�Wl�ˉ�B|i�|y      v   4  x����n�AE�٧H������3D���,"!�����g� "fg�w��G{־��kNn�������o�nr9�����-�C^ӷ����sz���_�HoW��@M�WP��UP��U3P��UP��U+PE�ڀ�,a��2kk�ZHX�R�h�5Mm�����(�ښ��J��L�M򮦪	���W��j�����͒�\ڣ\�}i޻��ҼwE}_S�?�E�������4��q5�b�!@�e���;����3'4���%�]���gp���ӞS��nNM0l'�9�Թ��s<����Djt?�	-0z��ƕ���w��z�6��+�6��+�&[oڠ�	���5�t{�&;n��.0{��d��~|{>�x|{g�r��������;�����d�X�9�_��~��>�_������/+�9O���'�Z�;�pQj�'���S�"\���y���X��FzrR�95������ Rrzρ=�tރ���hރ`� \x���߃�49�� HM��=VghM��� \�AlA�p���,߃"��T{5(�ګ@x�~�R)��>�RW{BP����R]�	E�n�pA�v4hE��&��T;����w(�(����!��T;�6����:�	��m�f+Ju�l�̾�xw��i����^��֎��=kǁ��Y�q �sRw8���r&(휉F'b��$YG��͙8��4��a@�i"�ÀZ*H���i�(���U'�*ŕ�KԜ+��|@�@����t��������7��(+�'�����d�Xp��ғc`�zr �d-О�	�'�����d�X��k�_�=;�'�����d�X�\;,xOƐ�U�L��ˋ8"D�����宗v���v�߿����U��)%���o9�lE��#���*��G�Q|�g���Yd,g��.##��_�D�+e��2�R9�������#����/Gd|9�0(-8���i��?R��a�Z���ւs�l�� �`#���0��9����/9���o͹?�_k���\s���s8lל��!����U�����p�q�+�      {      x������ � �     