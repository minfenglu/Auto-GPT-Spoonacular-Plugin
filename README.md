# Auto-GPT Spoonacular Plugin
The Auto-GPT Spoonacular Plugin 


## 🔧 Plugin Installation

Follow these steps to configure the Auto-GPT Spoonacular Plugin:

### 1. Follow Auto-GPT-Plugins Installation Instructions
Follow the instructions as per the [Auto-GPT-Plugins/README.md](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/blob/master/README.md)

### 2. Locate the `.env.template` file
Find the file named `.env.template` in the main `/Auto-GPT` folder.

### 3. Create and rename a copy of the file
Duplicate the `.env.template` file and rename the copy to `.env` inside the `/Auto-GPT` folder.

### 4. Edit the `.env` file
Open the `.env` file in a text editor. Note: Files starting with a dot might be hidden by your operating system.

### 5. Add Spoonacular configuration settings
Append the following configuration settings to the end of the file:

```ini

################################################################################
### SPOONACULAR
################################################################################
SPOONACULAR_API_KEY=YOUR_API_KEY_HERE
```

### 6. Allowlist Plugin
In your `.env` search for `ALLOWLISTED_PLUGINS` and add this Plugin:

```ini
################################################################################
### ALLOWLISTED PLUGINS
################################################################################

#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTSpoonacularPlugin
```
## 🧪 Test the Auto-GPT Spoonacular Plugin

Experience the plugin's capabilities by testing it for recommending dishes and getting recipes.


1. **Configure Auto-GPT:**
   Set up Auto-GPT with the following parameters:
   - Name: `ChefGPT`
   - Role: `Recommend`
   - Goals:
     1. Goal 1: `Ask user for query value`
     2. Goal 2: `Search recipes by user query using spoonacular plugin`
     3. Goal 3: `Ask user to select recipe id`
     4. Goal 4: `Terminate` 

A sample `ai_settins.yaml` 
```
ai_goals:
- Ask user for query value
- Search recipes by user query using spoonacular plugin
- Ask user to select recipe id
- Get recipe instructions by user-provide recipe id  
- Terminate
ai_name: ChefGPT
ai_role: Recommend
```



2. **Run Auto-GPT:**
   Launch Auto-GPT, which should use spooncacular plugin to give dish recommendations and recipes. 
